from blueshed.micro.orm import db_connection
from blueshed.micro.utils.base_context import BaseContext

from dogooder.model.user import User


class Context(BaseContext):
    """Extend BaseContext to include a db session."""

    def __init__(self, client_id, action_id, action, cookies=None, handler=None):  # noqa
        super().__init__(client_id, action_id, action, cookies=cookies, handler=handler)  # noqa
        self.headers  = handler.request.headers if handler and handler.request else None  # noqa
        self.settings = handler.settings if handler and handler.settings else None  # noqa

    @property
    def session(self):
        return db_connection.session()

    @property
    def current_user(self):
        """
        Returns the user object or None based on the clients
        current cookie state.

        The user returned is an expunged object so needs to be
        added to a new session if property access is required.

        This provides no user access control - use authenticated
        decorator in utils or handle in action.
        """
        with self.session as session:
            if self.current_user_id:
                user = session.query(User).get(self.current_user_id)
                session.expunge(user)
                return user
            return None

    @property
    def current_user_id(self):
        return self.get_cookie('current_user', None)

    @current_user_id.setter
    def current_user_id(self, user_id):
        self.set_cookie('current_user', user_id)
