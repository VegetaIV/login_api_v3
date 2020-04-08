from aiohttp.web import json_response
from json.decoder import JSONDecodeError
from errors import *
import elastic
import redisconnect
import uuid


class RouterHandler(object):
    def __init__(self, loop):
        self.loop = loop

    async def create_user(self, request):
        body = await decode_request(request)
        required_fields = ['username', 'email', 'password']
        await validate_fields(required_fields, body)

        username = body.get('username')
        user = await elastic.get_user_by_username(username)
        if user:
            return json_response({
                "status": "Failure",
                "detail": "User already existed"
            })
        else:
            user_id = str(uuid.uuid4())

        await elastic.create_user(
            username=username,
            mail=body.get('email'),
            password=body.get('password'),
            id=user_id
        )
        return json_response({
            "status": "Success",
            "detail": "User created",
            "userId": user_id
        })

    async def login(self, request):
        body = await decode_request(request)
        required_fields = ['username', 'password']
        await validate_fields(required_fields, body)

        username = body.get('username')
        password = body.get('password')
        user = await elastic.get_user_by_username(username)
        if len(user) == 0:
            return json_response({
                "status": "Failure",
                "detail": "User does not exist"
            })

        if not password == user['password']:
            return json_response({
                "status": "Failure",
                "detail": "Wrong password"
            })

        # await redisconnect.cache_set_user(username, password)
        user_id = user.get('id')

        return json_response({"result": "Success", "statusCode": 0, 'authorization': user_id})

    async def get_user_info(self, request):
        body = await decode_request(request)
        required_fields = ['id']
        await validate_fields(required_fields, body)
        try:
            id = request.rel_url.query['id']
        except:
            raise ApiBadRequest("'id' parameter is required")

        check = await redisconnect.check(id)
        if check:
            user = await redisconnect.cache_get_user(id)
            return json_response(
                user
            )
        else:
            return json_response({
                "status": "Failure",
                "detail": "Id incorrect"
            })

    async def set_user_info(self, request):
        body = await decode_request(request)
        required_fields = ['id', 'username', 'email']
        await validate_fields(required_fields, body)

        user_id = body.get('id')
        username = body.get('username')
        email = body.get('email')

        await redisconnect.cache_set_user(user_id, username, email)
        return json_response({
            "status": "Saved in redis",
            "id": user_id
        })


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


async def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest("'{}' parameter is required".format(field))
