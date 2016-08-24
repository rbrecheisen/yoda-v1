from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from lib.util import datetime_to_str

Base = declarative_base()


# ----------------------------------------------------------------------------------------------------------------------
class BaseModel(Base):

    __tablename__ = 'base'

    # User ID in database
    id = Column(Integer, primary_key=True)
    # Created by user
    created_by = Column(Integer, nullable=True)
    # Created at date and time
    created_at = Column(DateTime(timezone=True), default=func.now())
    # Updated by user
    updated_by = Column(Integer, nullable=True)
    # Updated at date and time
    updated_at = Column(DateTime(timezone=True), default=func.now())
    # Model type
    model_type = Column(String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'base',
        'polymorphic_on': model_type,
    }

    def to_dict(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'created_at': datetime_to_str(self.created_at),
            'updated_by': self.updated_by,
            'updated_at': datetime_to_str(self.updated_at),
        }

