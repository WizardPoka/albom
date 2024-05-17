# ====================================================================================
from fastapi import HTTPException

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .database_models import Base, WeekModel, GroupModel, DayModel, LessonModel

# ====================================================================================

def start_database():
    global SessionLocal
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

# Функция для сохранения расписания в базе данных
def save_schedule_to_db(schedule_data):
    db = SessionLocal()
    try:
        # Удаляем старые записи перед добавлением нового расписания
        db.query(LessonModel).delete()
        db.query(DayModel).delete()
        db.query(GroupModel).delete()
        db.query(WeekModel).delete()
        db.commit()

        # Проверка, что данные действительно удалены
        lesson_count = db.query(LessonModel).count()
        day_count = db.query(DayModel).count()
        group_count = db.query(GroupModel).count()
        week_count = db.query(WeekModel).count()
        print(f"Records after delete - Lessons: {lesson_count}, Days: {day_count}, Groups: {group_count}, Weeks: {week_count}")

        # Добавляем новое расписание
        for week_data in schedule_data:
            week = WeekModel(week=week_data.week)
            db.add(week)
            db.commit()
            db.refresh(week)
            for group_data in week_data.groups:
                group = GroupModel(group=group_data.group, week_id=week.id)
                db.add(group)
                db.commit()
                db.refresh(group)
                for day_data in group_data.days:
                    day = DayModel(day=day_data.day, group_id=group.id)
                    db.add(day)
                    db.commit()
                    db.refresh(day)
                    for lesson_data in day_data.lessons:
                        lesson = LessonModel(number=lesson_data.number, time_lesson=lesson_data.time_lesson,
                                             lesson=lesson_data.lesson, teacher=lesson_data.teacher,
                                             classroom=lesson_data.classroom, day_id=day.id)
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
from ..pydantic_model import Week, Group, Day, Lesson
def read_all_schedule_from_db() -> List[Week]:
    db = SessionLocal()
    weeks = []
    db_weeks = db.query(WeekModel).all()
    for db_week in db_weeks:
        groups = []
        db_groups = db.query(GroupModel).filter(GroupModel.week_id == db_week.id).all()
        for db_group in db_groups:
            days = []
            db_days = db.query(DayModel).filter(DayModel.group_id == db_group.id).all()
            for db_day in db_days:
                lessons = []
                db_lessons = db.query(LessonModel).filter(LessonModel.day_id == db_day.id).all()
                for db_lesson in db_lessons:
                    lesson = Lesson(
                        number=db_lesson.number,
                        time_lesson=db_lesson.time_lesson,
                        lesson=db_lesson.lesson,
                        teacher=db_lesson.teacher,
                        classroom=db_lesson.classroom
                    )
                    lessons.append(lesson)
                day = Day(day=db_day.day, lessons=lessons)
                days.append(day)
            group = Group(group=db_group.group, days=days)
            groups.append(group)
        week = Week(week=db_week.week, groups=groups)
        weeks.append(week)
    db.close()
    return weeks

# def read_all_schedule_from_db():
#     db = SessionLocal()
#     group_schedule = []
#     groups = db.query(GroupModel).all()
#     for group in groups:
#         group_data = {"group": group.group, "week": group.week.week, "days": []}
#         days = db.query(DayModel).filter(DayModel.group_id == group.id).all()
#         for day in days:
#             day_data = {"day": day.day, "lessons": []}
#             lessons = db.query(LessonModel).filter(LessonModel.day_id == day.id).all()
#             for lesson in lessons:
#                 lesson_data = {"number": lesson.number, "time_lesson": lesson.time_lesson,
#                                "lesson": lesson.lesson, "teacher": lesson.teacher,
#                                "classroom": lesson.classroom}
#                 day_data["lessons"].append(lesson_data)
#             group_data["days"].append(day_data)
#         group_schedule.append(group_data)
#     db.close()
#     return group_schedule

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