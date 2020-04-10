from zmq.asyncio import ZMQEventLoop
from aiohttp import web
from router_handler import RouterHandler
import asyncio
import logging
import argparse
import sys

LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Starts login_api')

    parser.add_argument(
        '-B', '--bind',
        help='identify host and port for api to run on',
        default='localhost:8000')
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='enable more verbose output to stderr')

    return parser.parse_args(args)


def start_server(host, port):
    _loop = asyncio.get_event_loop()

    app = web.Application(loop=_loop, client_max_size=20*1024**2)
    handler = RouterHandler(_loop)

    app.router.add_post('/create_user', handler.create_user)
    app.router.add_post('/login', handler.login)
    app.router.add_route('GET', '/user', handler.get_user_info)
    app.router.add_post('/cache_user', handler.set_user_info)

    LOGGER.info("Starting login_api on %s:%s", host, port)
    web.run_app(
        app,
        host=host,
        port=port,
        access_log=LOGGER,
        access_log_format="%r: %s status, %b size, in %Tf s"
    )


def main():
    print("__login-api__")
    loop = ZMQEventLoop()
    asyncio.set_event_loop(loop)

    try:
        opts = parse_args(sys.argv[1:])
        try:
            host, port = opts.bind.split(":")
            port = int(port)
        except ValueError:
            print("Unable to parse binding {}: Must be in the format"
                  " host:port".format(opts.bind))
            sys.exit(1)

        start_server(host, port)
    except Exception as err:
        LOGGER.exception(err)
        sys.exit(1)


