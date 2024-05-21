# uvicorn server.main:app --reload

# ====================================================================================

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import re
import io  # Импортируем модуль io
from io import BytesIO

from collections import defaultdict

from .pydantic_model import Week, Group, Day, Lesson
from .database.database_functions import (start_database, 
                                          read_all_schedule_from_db, 
                                          read_schedule_from_db, 
                                          save_schedule_to_db, 
                                          compare_schedules, 
                                          read_all_groups_from_db)
# ====================================================================================

app = FastAPI()

# Разрешить все источники
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ====================================================================================

start_database()

# ====================================================================================

def parse_text(value: str):

    pattern = re.compile(r'^(.*?)\s+([А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ]\.\s?[А-ЯЁ]\.)?)\s+(.*)$')
    match = pattern.search(value)

    if value == "Военный учебный цент . Воен. к":
        return ["Военный учебный цент." , "." , "Воен. к."]
    
    elif value == "Военный учебный цент ... Воен. к":
        return ["Военный учебный цент." , "." , "Воен. к."]
    
    elif match:
        extracted_text = match.group(1)
        last_name_with_initials = match.group(2)
        cabinet_or_website = match.group(3)
        return [extracted_text, last_name_with_initials, cabinet_or_website]
    
    else:
        return [value, None, None]

def get_time_for_pair(pair_number: str) -> str:
    time_mapping = {
        "1 пара": "09:00 - 10:35",
        "2 пара": "10:45 - 12:20",
        "3 пара": "13:00 - 14:35",
        "4 пара": "14:45 - 16:20",
        "5 пара": "16:30 - 18:05",
        "6 пара": "18:15 - 19:50",
        "7 пара": "20:00 - 21:35"
    }
    return time_mapping.get(pair_number, "")

# В вашем интерфейсе добавьте элемент с классом time_lesson и отобразите там время урока

    
# ====================================================================================

async def parse_excel(file: UploadFile = File(...)) -> Week:
    try:
        # Читаем данные из временного файла и передаем их в pd.read_excel()
        df = pd.read_excel(io.BytesIO(file.file.read()))
        
        # Заменяем значения NaN на предыдущий день недели (если есть), начиная с понедельника
        days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        current_day = None
        for i, row in df.iterrows():
            if pd.notnull(row['День']):
                current_day = row['День']
            else:
                df.at[i, 'День'] = current_day
        
        # Заменяем оставшиеся значения NaN на последний день недели (воскресенье)
        df['День'].ffill(inplace=True)

         # Создаем список для хранения всех Week объектов
        all_weeks = []

        # Разделяем расписание на две недели
        first_week_df = df.iloc[:df[df['День'] == 'Сб'].index[0] + 7]
        second_week_df = df.iloc[df[df['День'] == 'Сб'].index[0] + 7:]

        # Проходим по столбцам, начиная с третьего, для первой недели
        first_week_schedule = {}
        for i, row in first_week_df.iterrows():
            lesson_info = {}
            lesson_info['Урок'] = row['Урок']
            for column, value in row.iloc[2:].items():
                if pd.notnull(value):
                    if column in first_week_schedule:
                        if row['День'] in first_week_schedule[column]:
                            first_week_schedule[column][row['День']].append((row['Урок'], parse_text(value)))
                        else:
                            first_week_schedule[column][row['День']] = [(row['Урок'], parse_text(value))]
                    else:
                        first_week_schedule[column] = {row['День']: [(row['Урок'], parse_text(value))]}

        # Проходим по столбцам, начиная с третьего, для второй недели
        second_week_schedule = {}
        for i, row in second_week_df.iterrows():
            lesson_info = {}
            lesson_info['Урок'] = row['Урок']
            for column, value in row.iloc[2:].items():
                if pd.notnull(value):
                    if column in second_week_schedule:
                        if row['День'] in second_week_schedule[column]:
                            second_week_schedule[column][row['День']].append((row['Урок'], parse_text(value)))
                        else:
                            second_week_schedule[column][row['День']] = [(row['Урок'], parse_text(value))]
                    else:
                        second_week_schedule[column] = {row['День']: [(row['Урок'], parse_text(value))]}
        
        # Создаем Week объекты для каждой недели и добавляем их в список
        first_week = create_week_object("Первая неделя", first_week_schedule)
        second_week = create_week_object("Вторая неделя", second_week_schedule)
        all_weeks.extend([first_week, second_week])

        return all_weeks

    except Exception as e:
        print(f"Error in parse_excel: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ====================================================================================

def create_week_object(week_name: str, week_schedule: dict) -> Week:
    # Создаем словарь для хранения групп по названию
    group_dict = defaultdict(list)

    # Проходим по данным и формируем списки уроков для каждой группы
    for group, group_schedule in week_schedule.items():
        for day, day_schedule in group_schedule.items():
            lessons = []
            for lesson_info in day_schedule:
                classroom = lesson_info[1][2] if lesson_info[1][2] is not None else ""
                teacher = lesson_info[1][1] if lesson_info[1][1] is not None else ""
                lesson_number = lesson_info[0]
                time_lesson = get_time_for_pair(lesson_number)
                lesson = Lesson(
                    number=lesson_number,
                    time_lesson=time_lesson,
                    lesson=lesson_info[1][0],
                    teacher=teacher,
                    classroom=classroom
                )
                lessons.append(lesson)
            # Обновляем объект Group для каждой группы
            group_dict[group].append((day, lessons))

    # Формируем объекты Group из словаря групп
    all_groups = []
    for group_name, day_lessons_list in group_dict.items():
        group_days = defaultdict(list)
        for day, lessons in day_lessons_list:
            group_days[day].extend(lessons)
        days = [Day(day=day, lessons=lessons) for day, lessons in group_days.items()]
        group = Group(group=group_name, days=days)
        all_groups.append(group)

    # Формируем объект Week с полученными группами
    return Week(week=week_name, groups=all_groups)


# ====================================================================================

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        global schedule_data
        parsed_data = await parse_excel(file)
        schedule_data = parsed_data
        
        # save_schedule_to_db(schedule_data)
        schedule_data = read_all_schedule_from_db()
        return schedule_data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# ====================================================================================

@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    print(f"An error occurred: {repr(exc)}")
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

# ====================================================================================

@app.get("/schedule/group/{group}")
async def get_group_schedule(group: str):
    group_schedule = read_schedule_from_db(group)
    print(group_schedule)
    if not group_schedule:
        raise HTTPException(status_code=404, detail=f"Расписание для группы '{group}' не найдено")
    return group_schedule





@app.get("/groups/")
async def get_all_groups():
    all_groups = read_all_groups_from_db()
    if not all_groups:
        raise HTTPException(status_code=404, detail="Группы не найдены")
    return all_groups

