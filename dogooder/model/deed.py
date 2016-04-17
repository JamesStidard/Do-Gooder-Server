from sqlalchemy.types import String, Integer
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship

from dogooder.model.base import Base


class Deed(Base):
    id              = Column(Integer, primary_key=True)
    description     = Column(String(255), nullable=False, unique=True)
    accomplishments = relationship('Accomplishment',
                                   uselist=True,
                                   primaryjoin='Deed.id==Accomplishment.deed_id',  # noqa
                                   remote_side='Accomplishment.deed_id',
                                   back_populates='deed',
                                   cascade='all, delete-orphan')

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'accomplishments': [a.to_json() for a in self.accomplishments]
        }
