import datetime

from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship

from dogooder.model.base import Base


class Deed(Base):
    id              = Column(Integer, primary_key=True)
    description     = Column(String(255), nullable=False, unique=True)
    created         = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    accomplishments = relationship('Accomplishment',
                                   uselist=True,
                                   primaryjoin='Deed.id==Accomplishment.deed_id',  # noqa
                                   remote_side='Accomplishment.deed_id',
                                   back_populates='deed',
                                   cascade='all, delete-orphan')
    todays_accomplishments = relationship('Accomplishment',
                                          uselist=True,
                                          primaryjoin='and_(Deed.id==Accomplishment.deed_id, \
                                                            cast(Accomplishment.completed, Date) == func.current_date())')  # noqa

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
        }
