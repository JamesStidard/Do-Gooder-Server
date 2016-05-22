import logging

from tornado.escape import json_decode, json_encode

from blueshed.micro.utils.json_utils import dumps
from blueshed.micro.web.rpc_websocket import RpcWebsocket as Base

from dogooder.views.user import detailed_user_view


LOGGER = logging.getLogger(__name__)


class RpcWebsocket(Base):

    def __init__(self, *args, **kwargs):
        super(RpcWebsocket, self).__init__(*args, **kwargs)
        self._websocket_user = None

    def open(self, *args, **kwargs):
        super(RpcWebsocket, self).open(self, *args, **kwargs)

        # Send back a message containing details of the current logged in user
        context = self.micro_context(self._client_id, None, 'get_user', self._cookies_, self)  # noqa
        user    = context.current_user

        # If there is no user cookie set on this domain
        # Request a cookie stored on remote domain
        if user:
            self.write_message(dumps({
                "signal": 'CURRENT_USER_SET',
                "message": detailed_user_view(user) if user else None,
            }))
        else:
            self.write_message(dumps({
                "signal": 'MICRO_COOKIE_GET',
                "message": {"cookie_name": self.cookie_name}
            }))

    def on_message(self, message):
        data         = json_decode(message)
        cookie_value = [kwargs['value'] for (_, action, kwargs) in data.get("requests") if action == "MICRO_COOKIE_SET"]

        if cookie_value:
            user_id = self.get_secure_cookie(self.cookie_name, cookie_value[0])
            user_id = json_decode(user_id.decode('utf-8')) if user_id else None
            self._cookies_['current_user'] = user_id
            setattr(self, '_current_user', user_id)
            context = self.micro_context(self._client_id, None, 'get_user', self._cookies_, self)
            self.write_message(dumps({
                "signal": 'CURRENT_USER_SET',
                "message": detailed_user_view(context.current_user) if user_id else None,
            }))

        other_requests = [(id_, action, kwargs) for (id_, action, kwargs) in data.get("requests") if action != "MICRO_COOKIE_SET"]
        message        = json_encode({"requests": other_requests})

        super(RpcWebsocket, self).on_message(message)

    # def get_current_user(self):
    #     if self._websocket_user:
    #         return self._websocket_user
    #     else:
    #         return super(RpcWebsocket, self).get_current_user()
    #
    # def set_current_user(self, value):
    #     self._websocket_user = value
