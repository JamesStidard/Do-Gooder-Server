import logging

from tornado.web import Application
from tornado import ioloop

from dogooder.control import Control
from dogooder.handlers.websocket_handler import WebSocketHandler
from dogooder.utils.config import CONFIG


ROUTES = [
    (r"/websocket/?", WebSocketHandler, {'origins': CONFIG.ORIGINS}),
]


def main():
    # Construct the Control which will handle all actions performed by clients
    control = None  # Control(CONFIG.DB_URL, pool_recycle=60)

    # Create the web server application with eviroment settings
    app = Application(
        ROUTES,
        control=control,
        debug=CONFIG.DEBUG,
        cookie_name=CONFIG.COOKIE_NAME,
        cookie_secret=CONFIG.COOKIE_SECRET,
    )
    app.listen(CONFIG.PORT)
    logging.info('Listening on port {}'.format(CONFIG.PORT))

    # Keep any client websockets open by pinging them every now and then
    # ioloop.PeriodicCallback(WebSocketHandler.keep_alive, 30000).start()
    # Start the server - execution blocks here while server runs
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
