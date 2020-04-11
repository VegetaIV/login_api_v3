from aiohttp import web
from router_handler import RouterHandler
import asyncio


def start_server(host, port):
    _loop = asyncio.get_event_loop()
    app = web.Application(loop=_loop)

    handler = RouterHandler(_loop)

    app.router.add_post('/create_user', handler.create_user)
    app.router.add_post('/login', handler.login)
    app.router.add_route('GET', '/user', handler.get_user_info)
    app.router.add_post('/cache_user', handler.set_user_info)

    web.run_app(
        app,
        host=host,
        port=port
    )


def main():
    print()
    print("__Hoang Thanh Lam__")
    print()

    host = 'localhost'
    port = 8096
    start_server(host, port)


if __name__ == '__main__':
    main()
