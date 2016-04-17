from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime
from sqlalchemy import func

from dogooder.model.base import Base
from dogooder.model.custom_types.uuid import UUID
from dogooder.utils.date_helpers import to_unix_time


class Accomplishment(Base):
    id        = Column(Integer, primary_key=True)
    completed = Column(DateTime, nullable=False, default=func.now())
    user_id   = Column(UUID, ForeignKey('user.id'))
    user      = relationship('User',
                             uselist=False,
                             primaryjoin='Accomplishment.user_id==User.id',
                             remote_side='User.id',
                             back_populates='accomplishments')
    deed_id   = Column(Integer, ForeignKey('deed.id'))
    deed      = relationship('Deed',
                             uselist=False,
                             primaryjoin='Accomplishment.deed_id==Deed.id',
                             remote_side='Deed.id',
                             back_populates='accomplishments')

    def to_json(self):
        completed = to_unix_time(self.completed) if self.completed else None

        return {
            'id': self.id,
            'completed': completed,
        }
