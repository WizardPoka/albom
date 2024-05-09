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

async def parse_excel(file: UploadFile = File(...)):
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

        # Создаем список для хранения расписания
        weeks_schedule = []
        
        # Разделяем расписание на две недели
        first_week_df = df.iloc[:df[df['День'] == 'Сб'].index[0] + 7]
        second_week_df = df.iloc[df[df['День'] == 'Сб'].index[0] + 7:]
        
        # Преобразуем данные для первой недели
        first_week_schedule = convert_schedule_format(first_week_df)
        weeks_schedule.append({"week": "Первая неделя", "groups": first_week_schedule})
        
        # Преобразуем данные для второй недели
        second_week_schedule = convert_schedule_format(second_week_df)
        weeks_schedule.append({"week": "Вторая неделя", "groups": second_week_schedule})
        
        return weeks_schedule
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Функция для преобразования формата расписания
def convert_schedule_format(df):
    schedule = []
    group_column = None
    for column in df.columns:
        if 'группа' in column.lower():  # Проверяем, содержит ли имя столбца слово "группа"
            group_column = column
            break
    if group_column is None:
        raise ValueError("Столбец с названием группы не найден.")
    
    groups = df[group_column].unique()
    for group in groups:
        group_schedule = {"group": group, "days": []}
        group_df = df[df[group_column] == group]
        days = group_df['День'].unique()
        for day in days:
            day_schedule = {"day": day, "lessons": []}
            day_df = group_df[group_df['День'] == day]
            for index, row in day_df.iterrows():
                lesson = {
                    "number": row['Урок'],
                    "lesson": row['Предмет'],
                    "teacher": row['Преподаватель'],
                    "classroom": row['Аудитория']
                }
                day_schedule["lessons"].append(lesson)
            group_schedule["days"].append(day_schedule)
        schedule.append(group_schedule)
    return schedule

# ====================================================================================


schedule_data = None

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global schedule_data
    parsed_data = await parse_excel(file)
    schedule_data = parsed_data
    return parsed_data

# ====================================================================================

@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    print(f"An error occurred: {repr(exc)}")
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

# ====================================================================================

# @app.get("/schedule/{week}/{group}")
# async def get_group_schedule(week: str, group: str):
    
#     global schedule_data
    
#     if week == 'Первая неделя':
#         group_schedule = schedule_data['Первая неделя'].get(group)
#     elif week == 'Вторая неделя':
#         group_schedule = schedule_data['Вторая неделя'].get(group)
#     else:
#         return JSONResponse(content={"error": "Неверная неделя"}, status_code=400)
    
#     if group_schedule:
#         return JSONResponse(content=group_schedule, status_code=200)
#     else:
#         return JSONResponse(content={"error": "Расписание для выбранной группы не найдено"}, status_code=404)


@app.get("/schedule/group/{group}")
async def get_group_schedule(group: str):
    global schedule_data
    
    # Проверяем наличие группы в данных
    if group in schedule_data["Первая неделя"] and group in schedule_data["Вторая неделя"]:
        return {
            "Первая неделя": schedule_data["Первая неделя"].get(group),
            "Вторая неделя": schedule_data["Вторая неделя"].get(group)
        }
    elif group in schedule_data["Первая неделя"]:
        return {"Первая неделя": schedule_data["Первая неделя"].get(group)}
    elif group in schedule_data["Вторая неделя"]:
        return {"Вторая неделя": schedule_data["Вторая неделя"].get(group)}
    else:
        # Если группы нет в данных, возвращаем ошибку
        raise HTTPException(status_code=404, detail="Расписание для выбранной группы не найдено")