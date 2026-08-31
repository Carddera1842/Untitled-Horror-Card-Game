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


class EnemyModel(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    health = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    enemy_type = Column(String(50), nullable=False)
    