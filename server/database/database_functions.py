# database_functions.py

# ====================================================================================
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table, MetaData
from sqlalchemy import func

from .database_models import Base, WeekModel, GroupModel, DayModel, LessonModel

# ====================================================================================

def start_database():
    global SessionLocal
    global engine
    # Подключение к базе данных
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Проверьте подключение к базе данных
    try:
        # Создайте сессию
        db = SessionLocal()

        # Выполните простой запрос (например, подсчет количества записей в таблице WeekModel)
        count = db.query(WeekModel).count()
        # Выведите результат
        print("Подключение к базе данных установлено успешно!")
        print("Количество строк в таблице:", count)

        # Закройте сессию
        db.close()
    except Exception as e:
        print("Ошибка при подключении к базе данных:", e)

    # Создание таблиц в базе данных
    Base.metadata.create_all(bind=engine)

# ====================================================================================

def recreate_groups_table():
    meta = MetaData()
    groups_table = Table('groups', meta, autoload_with=engine)
    groups_table.drop(engine)
    Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables['groups']])

def save_schedule_to_db(schedule_data):
    db = SessionLocal()
    try:
        # Удаление старых данных
        db.query(LessonModel).delete()
        db.query(DayModel).delete()
        db.query(GroupModel).delete()
        db.query(WeekModel).delete()
        db.commit()

        # Пересоздание таблицы groups
        recreate_groups_table()

        print("Old records deleted and groups table recreated")

        for week_data in schedule_data:
            week = WeekModel(week=week_data.week)  # Использование week_data.week вместо week_data['week']
            db.add(week)
            db.commit()
            db.refresh(week)

            for group_data in week_data.groups:  # Использование week_data.groups вместо week_data['groups']
                group = GroupModel(group=group_data.group, week_id=week.id)  # Использование group_data.group вместо group_data['group']
                db.add(group)
                db.commit()
                db.refresh(group)

                for day_data in group_data.days:  # Использование group_data.days вместо group_data['days']
                    day = DayModel(day=day_data.day, group_id=group.id)  # Использование day_data.day вместо day_data['day']
                    db.add(day)
                    db.commit()
                    db.refresh(day)

                    for lesson_data in day_data.lessons:  # Использование day_data.lessons вместо day_data['lessons']
                        lesson = LessonModel(
                            number=lesson_data.number,  # Использование lesson_data.number вместо lesson_data['number']
                            time_lesson=lesson_data.time_lesson,  # Использование lesson_data.time_lesson вместо lesson_data['time_lesson']
                            lesson=lesson_data.lesson,  # Использование lesson_data.lesson вместо lesson_data['lesson']
                            teacher=lesson_data.teacher,  # Использование lesson_data.teacher вместо lesson_data['teacher']
                            classroom=lesson_data.classroom,  # Использование lesson_data.classroom вместо lesson_data['classroom']
                            day_id=day.id
                        )
                        db.add(lesson)
                        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
        
# ====================================================================================

def read_schedule_from_db(group):
    db = SessionLocal()
    group_schedule = []
    
    try:
        weeks = db.query(WeekModel).all()

        for week in weeks:
            week_data = {"week": week.week, "groups": []}
            groups = db.query(GroupModel).filter(GroupModel.group == group, GroupModel.week_id == week.id).all()
            for group_obj in groups:
                group_data = {"group": group_obj.group, "days": []}
                days = db.query(DayModel).filter(DayModel.group_id == group_obj.id).all()
                for day in days:
                    day_data = {"day": day.day, "lessons": []}
                    lessons = db.query(LessonModel).filter(LessonModel.day_id == day.id).all()
                    for lesson in lessons:
                        lesson_data = {
                            "number": lesson.number,
                            "time_lesson": lesson.time_lesson,
                            "lesson": lesson.lesson,
                            "teacher": lesson.teacher,
                            "classroom": lesson.classroom
                        }
                        day_data["lessons"].append(lesson_data)
                    group_data["days"].append(day_data)
                week_data["groups"].append(group_data)
            group_schedule.append(week_data)
    
    finally:
        db.close()
    
    return group_schedule

# ====================================================================================

def read_all_schedule_from_db():
    db = SessionLocal()
    all_schedule = []
    
    try:
        weeks = db.query(WeekModel).all()

        for week in weeks:
            week_data = {"week": week.week, "groups": []}
            groups = db.query(GroupModel).filter(GroupModel.week_id == week.id).all()
            for group_obj in groups:
                group_data = {"group": group_obj.group, "days": []}
                days = db.query(DayModel).filter(DayModel.group_id == group_obj.id).all()
                for day in days:
                    day_data = {"day": day.day, "lessons": []}
                    lessons = db.query(LessonModel).filter(LessonModel.day_id == day.id).all()
                    for lesson in lessons:
                        lesson_data = {
                            "number": lesson.number,
                            "time_lesson": lesson.time_lesson,
                            "lesson": lesson.lesson,
                            "teacher": lesson.teacher,
                            "classroom": lesson.classroom
                        }
                        day_data["lessons"].append(lesson_data)
                    group_data["days"].append(day_data)
                week_data["groups"].append(group_data)
            all_schedule.append(week_data)
    
    finally:
        db.close()
    
    return all_schedule
# ====================================================================================

# выводит список групп
def read_all_groups_from_db():
    db = SessionLocal()
    all_groups = []
    
    try:
        groups = db.query(GroupModel).all()
        for group in groups:
            all_groups.append(group.group)
    
    finally:
        db.close()
    
    return all_groups

# ====================================================================================

def search_teachers_in_db(query: str):
    db = SessionLocal()
    try:
        teachers = db.query(LessonModel.teacher).filter(LessonModel.teacher.like(f'{query}%')).distinct().all()
        print(teachers)
        return [teacher[0] for teacher in teachers]
    finally:
        db.close()


def get_teacher_schedule_from_db(teacher: str):
    db = SessionLocal()
    teacher_schedule = []
    try:
        lessons = db.query(LessonModel).filter(LessonModel.teacher == teacher).all()
        for lesson in lessons:
            day = db.query(DayModel).filter(DayModel.id == lesson.day_id).first()
            group = db.query(GroupModel).filter(GroupModel.id == day.group_id).first()
            week = db.query(WeekModel).filter(WeekModel.id == group.week_id).first()
            teacher_schedule.append({
                "week": week.week,
                "group": group.group,
                "day": day.day,
                "number": lesson.number,
                "time_lesson": lesson.time_lesson,
                "lesson": lesson.lesson,
                "classroom": lesson.classroom
            })
        return teacher_schedule
    finally:
        db.close()