import logging

from concurrent.futures.process import ProcessPoolExecutor

from tornado.autoreload import add_reload_hook
from tornado import ioloop
from tornado.web import Application
from tornado.options import options

from blueshed.micro.orm import db_connection, orm_utils
from blueshed.micro.utils import executor
from blueshed.micro.utils.service import Service
from blueshed.micro.web.rpc_handler import RpcHandler

from dogooder import actions
from dogooder.handlers.rpc_websocket import RpcWebsocket
from dogooder.utils.load_config import load_config
from dogooder.actions.context import Context
from dogooder.utils.config import get_ws_origins_env


def make_app():
    logging.info(get_ws_origins_env())

    db_url = orm_utils.heroku_db_url(options.CLEARDB_DATABASE_URL)
    engine = db_connection.db_init(db_url)

    if options.DEBUG:
        orm_utils.create_all(orm_utils.Base, engine)

    if options.POOL_SIZE:
        micro_pool = ProcessPoolExecutor(options.POOL_SIZE)
        executor.pool_init(micro_pool)
        if options.DEBUG:
            add_reload_hook(micro_pool.shutdown)

    logging.info('Pool size: {}'.format(options.POOL_SIZE))

    request_handlers = [
        (r"/control(.*)", RpcHandler, {
            'http_origins': options.ORIGINS,
            'ws_url': options.WS_URL
        }),
        (r"/websocket/?", RpcWebsocket, {
            'ws_origins': get_ws_origins_env()
        }),
    ]

    return Application(
        request_handlers,
        services=Service.describe(actions),
        micro_context=Context,
        debug=options.DEBUG,
        allow_exception_messages=options.DEBUG,
        cookie_name=options.COOKIE_NAME,
        cookie_secret=options.COOKIE_SECRET,
        gzip=True,
    )


def main():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)1.1s %(asctime)s %(process)d %(thread)x  %(module)s:%(lineno)d] %(message)s")  # noqa
    logging.getLogger("micro.utils.service").setLevel(logging.WARN)
    logging.getLogger("micro.utils.pika_tool").setLevel(logging.WARN)

    load_config(".env")

    app = make_app()
    app.listen(options.PORT)
    logging.info("listening on port {}".format(options.PORT))

    ioloop.PeriodicCallback(RpcWebsocket.keep_alive, 30000).start()
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
