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
        
        # Выводим данные в терминале
        # print("Первая неделя:", first_week_schedule)
        # print("Вторая неделя:", second_week_schedule)
        # print(str(len(first_week_schedule.keys())))
        # first_week_schedule = str(len(first_week_schedule.keys()))
        
        return {"Первая неделя": first_week_schedule, "Вторая неделя": second_week_schedule}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

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