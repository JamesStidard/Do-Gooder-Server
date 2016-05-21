import datetime

from dateutil import tz

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship

from blueshed.micro.orm.orm_utils import Base


class Deed(Base):
    id              = Column(Integer, primary_key=True)
    description     = Column(String(255), nullable=False, unique=True)
    created         = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)  # noqa
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

    @classmethod
    def todays_deeds(cls, session, *, timezone=None):
        timezone    = tz.gettz(timezone)
        today       = datetime.datetime.now(tz=timezone)
        today_start = datetime.datetime(today.year, today.month, today.day)
        seed        = int(today.strftime('%Y%m%d'))

        return session.query(Deed)\
                      .options(joinedload(Deed.todays_accomplishments))\
                      .filter(Deed.created < today_start)\
                      .order_by(func.rand(seed))\
                      .limit(2)
