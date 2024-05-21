# database_functions.py

# ====================================================================================
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table, MetaData

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

def compare_schedules(schedule1, schedule2):
    if len(schedule1) != len(schedule2):
        print(f"Количество недель не совпадает: {len(schedule1)} vs {len(schedule2)}")
        return False

    for week1, week2 in zip(schedule1, schedule2):
        if week1.week != week2.week:
            print(f"Недели не совпадают: {week1.week} vs {week2.week}")
            return False

        if len(week1.groups) != len(week2.groups):
            print(f"Количество групп в неделе {week1.week} не совпадает: {len(week1.groups)} vs {len(week2.groups)}")
            return False

        for group1, group2 in zip(week1.groups, week2.groups):
            if group1.group != group2.group:
                print(f"Группы не совпадают: {group1.group} vs {group2.group}")
                return False

            if len(group1.days) != len(group2.days):
                print(f"Количество дней для группы {group1.group} не совпадает: {len(group1.days)} vs {len(group2.days)}")
                return False

            for day1, day2 in zip(group1.days, group2.days):
                if day1.day != day2.day:
                    print(f"Дни не совпадают: {day1.day} vs {day2.day} для группы {group1.group}")
                    return False

                if len(day1.lessons) != len(day2.lessons):
                    print(f"Количество уроков для дня {day1.day} группы {group1.group} не совпадает: {len(day1.lessons)} vs {len(day2.lessons)}")
                    return False

                for lesson1, lesson2 in zip(day1.lessons, day2.lessons):
                    if lesson1 != lesson2:
                        print(f"Уроки не совпадают для {day1.day} группы {group1.group}: {lesson1} vs {lesson2}")
                        return False

    return True

# ====================================================================================