from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    location = Column(String,nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer,nullable=False)
    image_id = Column(Integer)

    room = relationship('Rooms',back_populates='hotel')

    def __str__(self):
        return f'Отель {self.name}'



# class Rooms(Base):
#     __tablename__ = 'rooms'
#
#     id = Column(Integer,primary_key=True,nullable=False)
#     hotel_id = Column(ForeignKey('hotels.id'),nullable=False)
#     name = Column(String,nullable=False)
#     description = Column(String,nullable=True)
#     price = Column(Integer,nullable=False)
#     services = Column(JSON,nullable=True)
#     quantity = Column(Integer,nullable=False)
#     image_id = Column(Integer,nullable=False)