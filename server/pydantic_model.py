# pydantic_model.py

from pydantic import BaseModel
from typing import List

# Модель данных для урока
class Lesson(BaseModel):
    number: str
    time_lesson: str
    lesson: str
    teacher: str
    classroom: str
    
# Модель данных для дня недели
class Day(BaseModel):
    day: str
    lessons: List[Lesson]

# Модель данных для группы
class Group(BaseModel):
    group: str
    days: List[Day]

# Модель данных для недели
class Week(BaseModel):
    week: str
    groups: List[Group]
