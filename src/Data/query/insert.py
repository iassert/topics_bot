class INSERT:
    userbot = """
        INSERT INTO userbots
        VALUES ('{phone}', {creator_id}, {user_id}, {group_id})
    """

    topic = """
        INSERT INTO topics
        VALUES ({me_id}, {from_user_id}, {topic_id})
    """