import os
from collections import namedtuple

from dotenv import load_dotenv

from dogooder.utils.orm_utils import heroku_db_url


if os.path.isfile('.env'):
    load_dotenv('.env')


def get_debug_env():
    debug = os.getenv('DEBUG', '')
    return False if debug.lower() in ['', 'no', 'false', '0'] else True


def get_db_url_env():
    db_url = os.getenv('CLEARDB_DATABASE_URL')
    if not db_url:
        raise ValueError('Requires CLEARDB_DATABASE_URL environment variable')
    return heroku_db_url(db_url)


def get_origins_env():
    origins = os.getenv('ORIGINS', '').split(',')
    return [o.strip() for o in origins]


def get_cookie_name_env():
    return os.getenv('COOKIE_NAME', 'do-gooder')


def get_cookie_secret_env(default="don't-you-dare-tell-anyone"):
    debug  = get_debug_env()
    secret = os.getenv('COOKIE_SECRET', default)
    if not debug and secret == default:
        raise ValueError('Default cookie secret used on production. Please set COOKIE_SECRET environment variable')  # noqa


def get_port_env():
    return int(os.getenv('PORT', 8888))


Configuration = namedtuple(
    'Configuration',
    'DEBUG, DB_URL, ORIGINS, COOKIE_NAME, COOKIE_SECRET, PORT',
)


CONFIG = Configuration(
    DEBUG=get_debug_env(),
    DB_URL=get_db_url_env(),
    ORIGINS=get_origins_env(),
    COOKIE_NAME=get_cookie_name_env(),
    COOKIE_SECRET=get_cookie_secret_env(),
    PORT=get_port_env(),
)
