from tornado.web import HTTPError

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from dogooder.model.user import User
from dogooder.views.user import detailed_user_view


def sign_in(context: 'micro_context', email: str, password: str) -> dict:
    """
    Sign user into Auth with a cookie and provides OTP for authing other
    services.
    """
    with context.session as session:
        try:
            user = session.query(User)\
                          .filter(or_(User.email == email,
                                      User.username == email))\
                          .one()
            user.authenticate(password)
            session.commit()
        except (NoResultFound, ValueError):
            raise HTTPError(400, reason='Incorrect username or password')
        else:
            context.current_user_id = user.id
            return detailed_user_view(user)
