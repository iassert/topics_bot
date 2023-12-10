import asyncio

from aiogram.types      import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from pyrogram          import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types    import User, Message as pyroMessage

from .main import Main

from Accest.markups         import Markups
from Accest.translation.btr import btr
from Accest.translation.etr import etr
from Accest.translation.ttr import ttr
from Accest.translation.ntr import ntr

from Bot.bot     import Bot_
from Bot.userbot import UserBot
from Bot.client  import Client_

from Data.userbots import UserBots
from Data.topics   import Topics


lock = asyncio.Lock()


class FormAuth(StatesGroup):
    add_userbot  = State()
    add_code     = State()
    add_password = State()


class Auth: 
    __doc__ = Main.__doc__

    auth_processed_media_groups_ids = []


    async def send_add_userbot(message: Message, state: FSMContext) -> None:
        """
        >* - '*'
        ># - btr.t1.add_userbot
        >[] - Markups.start(btr.t1)

        <* FormAuth.add_userbot
        <# ttr.t2
        <[] - Markups.back(btr.t2)
        """

        await Bot_(message).answer(ttr.t2, reply_markup = Markups.back)
        await FormAuth.add_userbot.set()

    async def add_userbot(message: Message, state: FSMContext) -> None:
        """
        >* - FormAuth.add_userbot
        ># - 
        >[] - Markups.back(btr.t2)

        if ># == btr.t2.back 
            <** - Main.start {
                <* - finish
                <# - ttr.t1
                <[] - Markups.start(btr.t1)
            }

        <** - Auth.__send_add_code {
            <* FormAuth.add_code
            <# ttr.t3
        }
        """

        if message.text == btr.t2.back:
            return await Main.start(message, state)

        data = message.text.split('\n')
        len_data = len(data)

        if len_data < ntr.num_arg_userbot:
            return await Bot_(message).answer(etr.t1)
        
        if len_data > ntr.num_arg_userbot:
            return await Bot_(message).answer(etr.t2)
        
        phone, password = data
        app = UserBot(phone)

        if not await app.connect():
            await Bot_(message).answer(etr.t3)

        if not await app.phone(phone):
            await Bot_(message).answer(etr.t4)

        async with state.proxy() as data:
            data["phone"]    = phone
            data["password"] = password

        await Auth.__send_add_code(message, state)

        
    async def __send_add_code(message: Message, state: FSMContext) -> None:
        """
        <* FormAuth.add_code
        <# ttr.t3
        """
                
        await Bot_(message).answer(ttr.t3)
        await FormAuth.add_code.set()

    async def add_code(message: Message, state: FSMContext) -> None:
        """
        >* - FormAuth.add_code
        ># - 
        >[] - Markups.back(btr.t2)

        if ># == btr.t2.back 
            <** - Auth.send_add_userbot {
                <* FormAuth.add_userbot
                <# ttr.t2
                <[] - Markups.back(btr.t2)
            }

        if state_code == 1
            <# - etr.t6
            <** - Auth.__send_add_password {
                <* FormAuth.add_password
                <# ttr.t4
            }

        <** - Auth.__save_userbot {
            <* - finish
            <# - ttr.t5
            <[] - Markups.empty
        }
        """

        if message.text == btr.t2.back:
            return await Auth.send_add_userbot(message, state)

        async with state.proxy() as data:
            phone    = data["phone"]
            password = data["password"]

        app = UserBot(phone)
        state_code = await app.code(message.text)

        if state_code == 2:
            return await Bot_(message).answer(etr.t5)
        
        if state_code == 1:
            if not await app.password(password):
                await Bot_(message).answer(etr.t6)
                return await Auth.__send_add_password(message, state)

        await Auth.__save_userbot(message, state)


    async def __send_add_password(message: Message, state: FSMContext) -> None:
        """
        <* FormAuth.add_password
        <# ttr.t4
        """

        await Bot_(message).answer(ttr.t4)
        return await FormAuth.add_password.set()

    async def add_password(message: Message, state: FSMContext) -> None:
        """
        >* - FormAuth.add_password
        ># - 
        >[] - Markups.back(btr.t2)

        if ># == btr.t2.back 
            <** - Auth.__send_add_code {
                <* FormAuth.add_code
                <# ttr.t3
            }

        <** - Auth.__save_userbot {
            <* - finish
            <# - ttr.t5
            <[] - Markups.empty
        }
        """

        if message.text == btr.t2.back:
            return await Auth.__send_add_code(message, state)
        
        async with state.proxy() as data:
            phone    = data["phone"]

        app = UserBot(phone)
        if not await app.password(message.text):
            await Bot_(message).answer(etr.t6)

        await Auth.__save_userbot(message, state)


    async def __save_userbot(message: Message, state: FSMContext) -> None :
        """
        <* - finish
        <# - ttr.t5
        <[] - Markups.empty
        """

        async with state.proxy() as data:
            phone = data["phone"]
        app = UserBot(phone)

        await state.finish()
        await Bot_(message).answer(ttr.t5, reply_markup = Markups.empty)

        data_: list[str, int] | None = await app.custom_create_group()
        if data_ is None:
            return await Bot_(message).answer(etr.t7, reply_markup = Markups.start)

        link, group_id = data_
        
        me_ = await app.get_me()
        app_ = app.to_Client_()

        await Auth.__send_from_user_info(app_, me_, group_id)

        await Bot_(message).answer(ttr.t6.format(link))

        if not UserBots.add_userbot(phone, message.from_user.id, await app.get_user_id(), group_id):
            return await Bot_(message).answer(etr.t8, reply_markup = Markups.start)

        await Bot_(message).answer(ttr.t7)
        
        await app.disconnect()
        app.del_single_obj()

        asyncio.create_task(
            Auth._register_app_message_handler(phone, group_id)
        )

        await Bot_(message).answer(ttr.t8, reply_markup = Markups.start)


    async def _register_app_message_handler(phone: str, group_id: int) -> None:
        app = UserBot(phone)

        await app.start()

        app.add_handler(
            MessageHandler(
                Auth._app_get_message_handler, 
                filters.private & 
                ~filters.me &
                ~filters.media_group &
                (filters.text | filters.photo | filters.video | filters.video_note | filters.document)
            )
        )
        app.add_handler(
            MessageHandler(
                Auth._app_get_media_group_handler, 
                filters.private & 
                ~filters.me &
                filters.media_group
            )
        )

        app.add_handler(
            MessageHandler(
                Auth._app_send_message_handler, 
                filters.chat(group_id) & 
                ~filters.me &
                ~filters.media_group &
                (filters.text | filters.photo | filters.video | filters.video_note | filters.document)
            )
        )
        app.add_handler(
            MessageHandler(
                Auth._app_send_media_group_handler, 
                filters.chat(group_id) & 
                ~filters.me &
                filters.media_group
            )
        )

        await idle()
        await app.stop()


    async def _app_get_message_handler(client: Client, message: pyroMessage, *, is_media_group: bool = False) -> None:
        app = Client_(client)

        me = await client.get_me()
        me_id = me.id

        from_user_id    = message.from_user.id
        from_first_name = message.from_user.first_name
        
        from_contact = '. '.join(
            [i for i in [
                message.from_user.phone_number,
                message.from_user.username
            ] if i]
        )
        title = f"{from_first_name}. {from_contact}"

        kwargs = {
            "me_first_name": me.first_name,
            "me_phone": me.phone_number,
            "from_first_name": from_first_name,
            "from_contact": from_contact
        }

        group_id = UserBots.get_group_id(me_id)
        creator_id = UserBots.get_creator_id(me_id)

        if group_id is None:
            if creator_id is not None:
                await Bot_.send_message(creator_id, etr.t9.format(**kwargs))
            return

        topic_id = Topics.get_topic_id(me_id, from_user_id)
        if topic_id is None:
            topic_id_ = await app.create_topic(group_id, title)

            await Auth.__send_from_user_info(app, message.from_user, group_id, topic_id_)

            if topic_id_ is None:
                return await Bot_.send_message(creator_id, etr.t10.format(**kwargs))

            res = Topics.add_topic(me_id, from_user_id, topic_id_)
            if not res:
                return await Bot_.send_message(creator_id, etr.t11.format(**kwargs))
            topic_id = topic_id_

        if is_media_group:
            msg = await app.copy_media_group(group_id, message.chat.id, message.id)
        else:
            msg = await app.copy_message(group_id, message.chat.id, message.id, reply_to_message_id = topic_id)
        
        if msg is None:
            await Bot_.send_message(creator_id, etr.t12.format(**kwargs))

    async def _app_get_media_group_handler(client: Client, message: pyroMessage) -> None: 
        async with lock:
            if message.media_group_id in Auth.auth_processed_media_groups_ids:
                return
            Auth.auth_processed_media_groups_ids.append(message.media_group_id)

        await Auth._app_get_message_handler(client, message, is_media_group = True)


    async def _app_send_message_handler(client: Client, message: pyroMessage, *, is_media_group: bool = False) -> None:
        app = Client_(client)

        me = await client.get_me()
        me_id = me.id

        topic_id = message.reply_to_top_message_id 
        if topic_id is None:
            topic_id = message.reply_to_message_id

        from_user_id = Topics.get_from_user_id(me_id, topic_id)
        
        t = etr.t14
        if from_user_id is not None:
            if is_media_group:
                msg = await app.copy_media_group(from_user_id, message.chat.id, message.id)
            else:
                msg = await app.copy_message(from_user_id, message.chat.id, message.id)

            t = ttr.t9
            if msg is None:
                t = etr.t13

        await app.send_message(
            chat_id = message.chat.id,
            text = t,
            reply_to_message_id = message.id
        )

    async def _app_send_media_group_handler(client: Client, message: pyroMessage) -> None: 
        async with lock:
            if message.media_group_id in Auth.auth_processed_media_groups_ids:
                return
            Auth.auth_processed_media_groups_ids.append(message.media_group_id)

        await Auth._app_send_message_handler(client, message, is_media_group = True)


    async def __get_from_user_info(user: User) -> str:
        from_user_info = user.first_name
        if user.last_name:
            from_user_info += f"\n{user.last_name}"

        if user.phone_number:
            from_user_info += f"\n{user.phone_number}"

        if user.username:
            from_user_info += f"\n@{user.username}"

        return from_user_info

    async def __send_from_user_info(app: Client_, user: User, group_id: int, topic_id: int = 1) -> None:
        from_user_info = await Auth.__get_from_user_info(user)

        if user.photo:
            avatar = await app.download_media(user.photo.big_file_id, in_memory = True)
            if avatar:
                return await app.send_photo(group_id, avatar, from_user_info, reply_to_message_id = topic_id)
        await app.send_message(group_id, from_user_info, reply_to_message_id = topic_id)