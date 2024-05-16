from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .database_models import Base, WeekModel, GroupModel, DayModel, LessonModel

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

def save_schedule_to_db(schedule_data):
    db = SessionLocal()
    for week_data in schedule_data:
        week = WeekModel(week=week_data.week)
        db.add(week)
        db.commit()
        db.refresh(week)
        for group_data in week_data.groups:
            try:
                group = GroupModel(group=group_data.group, week_id=week.id)
                db.add(group)
                db.commit()
                db.refresh(group)
            except IntegrityError:
                db.rollback()  # Откатываем транзакцию в случае нарушения уникального ограничения
                existing_group = db.query(GroupModel).filter_by(group=group_data.group).first()
                group = existing_group
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
    db.close()


def read_schedule_from_db(group):
    db = SessionLocal()
    group_schedule = []
    groups = db.query(GroupModel).filter(GroupModel.group == group).all()
    for group in groups:
        group_data = {"group": group.group, "week": group.week.week, "days": []}
        days = db.query(DayModel).filter(DayModel.group_id == group.id).all()
        for day in days:
            day_data = {"day": day.day, "lessons": []}
            lessons = db.query(LessonModel).filter(LessonModel.day_id == day.id).all()
            for lesson in lessons:
                lesson_data = {"number": lesson.number, "time_lesson": lesson.time_lesson,
                               "lesson": lesson.lesson, "teacher": lesson.teacher,
                               "classroom": lesson.classroom}
                day_data["lessons"].append(lesson_data)
            group_data["days"].append(day_data)
        group_schedule.append(group_data)
    db.close()
    return group_schedule