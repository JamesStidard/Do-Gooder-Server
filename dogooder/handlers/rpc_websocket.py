import logging

from blueshed.micro.utils.json_utils import dumps
from blueshed.micro.web.rpc_websocket import RpcWebsocket as Super

from dogooder.views.user import detailed_user_view


LOGGER = logging.getLogger(__name__)


class RpcWebsocket(Super):

    def open(self, *args, **kwargs):
        super(RpcWebsocket, self).open(self, *args, **kwargs)

        # Send back a message containing details of the current logged in user
        context = self.micro_context(self._client_id, None, 'get_user', self._cookies_, self)  # noqa
        user    = context.current_user

        self.write_message(dumps({
            "signal": 'SET_CURRENT_USER',
            "message": detailed_user_view(user) if user else None,
        }))
