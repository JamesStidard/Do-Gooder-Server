import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Boolean, Integer
from sqlalchemy.schema import Column

from utilise.password_helper import PasswordHelper as PWH

from blueshed.micro.orm.orm_utils import Base

from dogooder.model.custom_types.uuid import UUID


class User(Base):
    id                 = Column(Integer, primary_key=True)
    username           = Column(String(255), nullable=False, unique=True)
    _email             = Column('email', String(255), nullable=False, unique=True)  # noqa
    email_confirmed    = Column(Boolean, nullable=False, default=False)
    confirmation_token = Column(UUID, unique=True, default=uuid.uuid4)
    _password          = Column('password', String(255), nullable=False)
    accomplishments    = relationship('Accomplishment',
                                      uselist=True,
                                      primaryjoin='User.id==Accomplishment.user_id',  # noqa
                                      remote_side='Accomplishment.user_id',
                                      back_populates='user',
                                      cascade='all, delete-orphan')
    type               = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self.email_confirmed    = False
        self.confirmation_token = uuid.uuid4()
        self._email             = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = PWH.create_password(password)

    def authenticate(self, password: str=None):
        success, updated_password = PWH.validate_password(self.password, password)  # noqa
        if not success:
            raise ValueError('Incorrect password')

        self._password = updated_password
        return success

    def change_password(self, password: str, *, new_password: str):
        success, self._password = PWH.change_password(self.password, password, new_password)  # noqa
        if not success:
            raise ValueError('Incorrect password')
        return success


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
