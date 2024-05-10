# uvicorn server.main:app --reload

# ====================================================================================

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import re
import io  # Импортируем модуль io
from io import BytesIO

import json
from typing import Dict, List
from pydantic import BaseModel, ValidationError
# ====================================================================================

# Модель данных для урока
class Lesson(BaseModel):
    number: str
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
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ====================================================================================

def create_week_object(week_name: str, week_schedule: dict) -> Week:
    # Создаем список для хранения всех Group объектов
    all_groups = []

    # Проходим по данным и формируем списки уроков для каждой группы
    for group, group_schedule in week_schedule.items():
        lessons = []
        for day, day_schedule in group_schedule.items():
            for lesson_info in day_schedule:
                classroom = lesson_info[1][2] if lesson_info[1][2] is not None else ""
                teacher = lesson_info[1][1] if lesson_info[1][1] is not None else ""  # добавляем проверку на None
                lesson = Lesson(
                    number=lesson_info[0],
                    lesson=lesson_info[1][0],
                    teacher=teacher,  # используем teacher вместо lesson_info[1][1]
                    classroom=classroom
                )
                lessons.append(lesson)
            # Формируем объект Day для каждого дня
            day_object = Day(day=day, lessons=lessons[:])  # копируем список уроков для каждого дня
            all_groups.append(Group(group=group, days=[day_object]))  # формируем объект Group для каждой группы

    # Формируем объект Week с полученными группами
    return Week(week=week_name, groups=all_groups)

# ====================================================================================



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        global schedule_data
        parsed_data = await parse_excel(file)
        schedule_data = parsed_data
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
    global schedule_data
    
    print(schedule_data)  # Для отладки - выводим данные о расписании в консоль
    
    if schedule_data is None:
        # Если данные о расписании не загружены, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Данные о расписании еще не загружены")
    
    if not isinstance(schedule_data, list):
        # Если данные о расписании не являются списком, возвращаем ошибку 500
        raise HTTPException(status_code=500, detail="Неправильный формат данных о расписании")
    
    # Поиск выбранной группы в данных о расписании
    for week in schedule_data:
        for group_data in week["groups"]:
            if group_data["group"] == group:
                return group_data
    
    # Если группа не найдена в данных, возвращаем ошибку 404
    raise HTTPException(status_code=404, detail="Расписание для выбранной группы не найдено")


