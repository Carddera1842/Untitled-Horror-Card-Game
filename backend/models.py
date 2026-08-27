from sqlalchemy import Column, Integer, String

from database import Base


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    damage = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)