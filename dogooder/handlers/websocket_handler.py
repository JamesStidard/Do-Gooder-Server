import time
import logging
from urllib.parse import urlparse
from json import dumps as json_encode

from tornado.websocket import WebSocketHandler as BaseHandler
from tornado.log import access_log
from tornado.web import create_signed_value
from tornado.escape import json_decode

from dogooder.utils.access_exception import AccessException


class WebSocketHandler(BaseHandler):

    def initialize(self, origins=None):
        super().initialize()
        self._origins_ = origins
        self._user_    = None

    def get_current_user(self):
        return self.get_secure_cookie(self.cookie_name)

    @property
    def control(self):
        return self.application.settings.get('control')

    @property
    def cookie_name(self):
        return self.application.settings.get('cookie_name')

    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = self.get_current_user()
        if self._current_user:
            return self._current_user

    def gen_login_cookie(self, value):
        return create_signed_value(self.application.settings["cookie_secret"],
                                   self.cookie_name, str(value))

    @property
    def user(self):
        return self._user_

    @user.setter
    def user(self, value):
        self._user_ = value
        self._current_user = value.get("id") if value else None
        if value:
            cookie = self.gen_login_cookie(self._current_user).decode("utf-8")
            self.write_message(json_encode({
                "signal": "user",
                "cookie": cookie,
                "cookie_name": self.cookie_name,
                "message": value
            }))

    def check_origin(self, origin):
        if self._origins_:
            parsed_origin = urlparse(origin)
            return parsed_origin.netloc in self._origins_
        return super().check_origin(origin)

    def open(self):
        self.control._clients.append(self)
        if self.current_user:
            logging.info("reopening user: %s", self.current_user)
            self.control._set_user(self, self.current_user)
            self.write_message(json_encode({
                "signal": "user",
                "message": self._user_,
            }))
        else:
            self.write_message(json_encode({
                "signal": "cookie",
                "message": {"cookie_name": self.cookie_name}
            }))

    def on_message(self, message):
        start    = time.time()
        requests = json_decode(message).get("requests", [])

        for request_id, action, args in requests:
            args = args if args else {}
            try:
                if action == "cookie":
                    value = self.get_secure_cookie(self.cookie_name,
                                                   args.get('value'))
                    if value:
                        self._current_user = value.decode('utf-8')
                        self.control._set_user(self, self.current_user)
                        self.write_message(json_encode({
                            "signal": "user",
                            "message": self._user_,
                        }))
                elif action == "logout":
                    self.user = None
                    self.write_message(json_encode({
                        "result": self.cookie_name,
                        "response_id": request_id
                    }))
                else:
                    if action[0] == "_":
                        raise AccessException("controlled method accessed")
                    method = getattr(self.control, action)
                    result = method(self, **args)
                    self.write_message(json_encode({
                        "result": result,
                        "response_id": request_id
                    }))
                    self.control._flush()
            except Exception as ex:
                logging.exception(ex)
                error = str(ex)
                self.write_message(json_encode({
                    "result": None,
                    "error": error,
                    "response_id": request_id
                }))
                self.log_action(access_log.error, start,
                                action, self.current_user, error)
                self.control._flush(ex)

    def log_action(self, logger, start, action, user, message=''):
        request_time = (time.time() - start) * 1000
        logger("%s - %s - %s - %sms" %
               (action, self.current_user, message, request_time))

    def on_close(self):
        self.control._clients.remove(self)

    def force_close(self, code=None, reason=None):
        self.control._clients.remove(self)
        self.close(code, reason)

    def broadcast(self, message):
        self.write_message(json_encode(message))
