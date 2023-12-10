from aiogram.bot.api import TelegramAPIServer


class Config:
    TOKEN: str
    CREATOR_ID: int = 704750195

    DATABASE: str = "topics_bot"
    USER:     str = "assert"
    PASSWORD: str = "KhERp2ni_ALpRMdv3paBJUG-hVOryTu0"
    HOST:     str
    PORT:     str = "5434"

    LOCAL_SERVER: TelegramAPIServer = TelegramAPIServer.from_base('http://localhost:8081')
