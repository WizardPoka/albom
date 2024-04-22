from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import re
import io  # Импортируем модуль io
from io import BytesIO
import json
from typing import Dict, List

app = FastAPI()

# # Регулярное выражение для извлечения текста, фамилии с инициалами и кабинета/веб-сайта
# pattern = re.compile(r'^(.*?)\s+([А-ЯЁ][а-яё]+ [А-ЯЁ]\. [А-ЯЁ]\.)\s+(.*)$')

# def fill_missing_days(df):
#     # Заменяем пропущенные значения в первом столбце дней недели
#     df.iloc[:, 0] = df.iloc[:, 0].ffill()

#     return df

def parse_excel(file: UploadFile = File(...)):
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
        df['День'].fillna(method='ffill', inplace=True)
        
        # Проходим по столбцам, начиная с третьего
        schedule_by_group = {}
        for i, row in df.iterrows():
            lesson_info = {}
            lesson_info['Урок'] = row['Урок']
            for column, value in row.iloc[2:].items():
                if pd.notnull(value):
                    if column in schedule_by_group:
                        if row['День'] in schedule_by_group[column]:
                            schedule_by_group[column][row['День']].append((row['Урок'], value))
                        else:
                            schedule_by_group[column][row['День']] = [(row['Урок'], value)]
                    else:
                        schedule_by_group[column] = {row['День']: [(row['Урок'], value)]}
        
        # Выводим данные в терминале
        print(schedule_by_group)
        
        return schedule_by_group
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    parsed_data = parse_excel(file)
    return parsed_data


@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    print(f"An error occurred: {repr(exc)}")
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)
