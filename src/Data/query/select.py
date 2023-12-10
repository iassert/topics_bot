class SELECT:
    phone_group_id_userbots = "SELECT phone, group_id FROM userbots;"
    group_id = """
        SELECT group_id
        FROM userbots
        WHERE user_id = {user_id}
        LIMIT 1;
    """
    creator_id = """
        SELECT creator_id
        FROM userbots
        WHERE user_id = {user_id}
        LIMIT 1;
    """
    topic_id = """
        SELECT topic_id
        FROM topics
        WHERE me_id = {me_id} AND from_user_id = {from_user_id}
        LIMIT 1;
    """
    from_user_id = """
        SELECT from_user_id
        FROM topics
        WHERE me_id = {me_id} AND topic_id = {topic_id}
        LIMIT 1;
    """