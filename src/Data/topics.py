from .db           import DB
from .query.create import CREATE
from .query.insert import INSERT
from .query.select import SELECT


class Topics:
    @staticmethod
    def add_topic(me_id: int, from_user_id: int, topic_id: int) -> bool:
        db_ = DB()
        
        if not db_.execute(INSERT.topic.format(
            me_id        = me_id, 
            from_user_id = from_user_id,
            topic_id     = topic_id
        )): return False

        if not db_.commit():
            return False
        
        return True

    
    @staticmethod
    def get_topic_id(me_id: int, from_user_id: int) -> int | None:
        db_ = DB()

        if not db_.execute(SELECT.topic_id.format(
            me_id        = me_id,
            from_user_id = from_user_id
        )): return

        res = db_.fetchone()
        if res is not None:
            return int(res[0])

    @staticmethod
    def get_from_user_id(me_id: int, topic_id: int) -> int | None:
        db_ = DB()

        if not db_.execute(SELECT.from_user_id.format(
            me_id    = me_id,
            topic_id = topic_id
        )): return

        res = db_.fetchone()
        if res is not None:
            return int(res[0])

db_ = DB()
db_.execute(CREATE.topics)
db_.commit()
