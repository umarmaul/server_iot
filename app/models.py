from .database import Base
from sqlalchemy import Column, Integer, Float, DateTime
import datetime

class Pzem(Base):
    __tablename__ = "pzem"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now)
    voltage = Column(Float)
    current = Column(Float)
    power = Column(Float)
    energy = Column(Float)
    frequency = Column(Float)
    power_factor = Column(Float)
    
class AHT10(Base):
    __tablename__ = "aht10"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now)
    temperature = Column(Float)
    humidity = Column(Float)

class Camera(Base):
    __tablename__ = "camera"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now)
    occupant = Column(Integer)
    
class OpenWeather(Base):
    __tablename__ = "open_weather"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now)
    temperature = Column(Float)
    humidity = Column(Float)