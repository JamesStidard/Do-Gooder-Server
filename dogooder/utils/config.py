from tornado.options import define, options

from blueshed.micro.utils.utils import url_to_ws_origins

define("ENV_REDIRECT",
       type=str,
       help="Allows for multiple enviroments to be used for development")

define("DEBUG",
       default=False,
       type=bool,
       help="Enables logging and returns stack trace erros to clients.")

define("CLEARDB_DATABASE_URL",
       type=str,
       help="The database connection string for SQLAlchemy.")

define("ORIGINS",
       multiple=True,
       help="These are the accepted CORS origins for the server.")

define("COOKIE_NAME",
       default="a2z-users",
       type=str,
       help="The name of the session cookie used in request headers.")

define("COOKIE_SECRET",
       default="don't-you-dare-tell-anyone",
       type=str,
       help="This is the secret used to sign the servers session cookies.")

define("PORT",
       default=8888,
       type=int,
       help="The port the server will open and listen for communications on.")

define("WS_URL",
       default="ws://localhost:8888/websocket",
       type=str,
       help="The full url for websocket connections.")

define("POOL_SIZE",
       default=0,
       type=int,
       help="The number of processes running to serve concurrent requests.")


def get_ws_origins_env():
    return [url_to_ws_origins(u) for u in options.ORIGINS]
