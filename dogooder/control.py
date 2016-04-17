from contextlib import contextmanager

from sqlalchemy.orm.exc import NoResultFound
from blueshed.model_helpers.base_control import BaseControl

from dogooder.utils.orm_utils import connect
from dogooder.model.user import User
from dogooder.model.deed import Deed


class Control(BaseControl):
    """
    Public Interface Definition and Implementation.

    Encapsulates a database connection and provides a session interface
    can generate passwords, contains a list of websocket clients and
    will broadcast state changes to interested client.
    """

    def __init__(self, db_url: str, echo: bool=False, pool_recycle=None):
        BaseControl.__init__(self, db_url, echo, pool_recycle)

        self._engine, self._Session = connect(db_url, echo, pool_recycle)
        self._clients = []
        self._pending = []

    @property
    @contextmanager
    def session(self):
        """Self closing session for use by with statements."""
        session = self._Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _broadcast(self, signal: str, message: str, accl=None):
        PUBLIC = None
        news   = {"signal": signal, "message": message}

        [client.broadcast(news)
         for client in self._clients
         if accl is PUBLIC or client.current_user in accl]

    def _broadcast_on_success(self, signal: str, message: str, accl=None):
        self._pending.append((signal, message, accl))

    def _broadcast_result_(self, signal: str, message: str, accl=None):
        self._broadcast_on_success(signal, message, accl)
        return message

    def _flush(self, error=None):
        """Called by clients after completing work."""
        if not error:
            for args in self._pending:
                self._broadcast(*args)
        self._pending = []

    def _set_user(self, client, person_id):
        """Called by client on authenticating."""
        with self.session as session:
            user = session.query(User).get(person_id)
            client.user = user.to_json()

    def ping(self, client):
        """Keep-alive Endpoint."""
        return "pong"

    def login(self, client, email, password):
        """Called by client to authenticate."""
        with self.session as session:
            try:
                user = session.query(User).filter(User._email == email).one()
                user.authenticate(password)
            except (NoResultFound, ValueError):
                raise Exception("Email or password incorrect")
            else:
                client.user = user.to_json()

    def get_deeds(self, client):
        with self.session as session:
            deeds = session.query(Deed).all()
            return [deed.to_json() for deed in deeds]

    def insert_deed(self, client, description):
        with self.session as session:
            deed = Deed(description=description)
            session.add(deed)
            session.flush()
            self._broadcast_on_success('insert_deed', deed.to_json())
        
