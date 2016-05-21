from tornado.options import options

from blueshed.micro.utils.config import load_config as _load_config


def load_config(path=None):
    redirect = True

    while redirect:
        _load_config(path)

        if options.ENV_REDIRECT and options.ENV_REDIRECT is not path:
            path = options.ENV_REDIRECT
        else:
            redirect = False
