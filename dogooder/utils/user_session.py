from functools import wraps

from dogooder.model import User


def user_session(f):
    @wraps(f)
    def call(self, client, *args, **kwargs):
        with self.session as session:
            session.info['client'] = client
            user = None
            id_  = client.current_user
            user = session.query(User).filter(User.id == id_).one()
            session.info['user'] = user
            result = f(self, user, session, *args, **kwargs)
        return result
    return call
