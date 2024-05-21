from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class WeekModel(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True, index=True)
    week = Column(String, unique=True)
    groups = relationship("GroupModel", back_populates="week")

class GroupModel(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String, unique=True)
    week_id = Column(Integer, ForeignKey('weeks.id'))

    week = relationship("WeekModel", back_populates="groups")
    days = relationship("DayModel", back_populates="group")

class DayModel(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship("GroupModel", back_populates="days")
    lessons = relationship("LessonModel", back_populates="day")

class LessonModel(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String)
    time_lesson = Column(String)
    lesson = Column(String)
    teacher = Column(String)
    classroom = Column(String)
    day_id = Column(Integer, ForeignKey('days.id'))

    day = relationship("DayModel", back_populates="lessons")
