import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
cache = redis.Redis(connection_pool=POOL)


async def cache_set_user(user_id, username, mail):
    cache.set("username", username)
    cache.set("mail", mail)
    cache.set("id", user_id)
    return user_id


async def cache_get_user(user_id):
    username = cache.get("username")
    mail = cache.get("mail")

    if username is None:
        return None

    body = {
        "id": user_id,
        "username": str(username, 'utf-8'),
        "mail": str(mail, 'utf-8')
    }
    return body


async def check(user_id):
    _user_id = str(cache.get("id"), 'utf-8')
    if user_id == _user_id:
        return True
    return False
