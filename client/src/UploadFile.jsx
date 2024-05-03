// UploadFile.jsx

// ====================================================================================

import React, { useState } from 'react';
import axios from 'axios';

// ====================================================================================

const UploadFile = () => {
  // Состояние для хранения выбранного файла
  const [file, setFile] = useState(null);
  // Состояние для хранения расписания, полученного с сервера
  const [schedule, setSchedule] = useState(null);

// ====================================================================================

  // Обработчик изменения файла
  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Обновляем состояние файла
  };

// ====================================================================================

  // Обработчик отправки файла на сервер
  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('file', file); // Добавляем файл в FormData

    try {
      // Отправляем файл на сервер
      const response = await axios.post('http://localhost:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data' // Устанавливаем заголовок для формы данных
        }
      });
      // Обновляем состояние расписания с данными, полученными с сервера
      setSchedule(response.data);
    } catch (error) {
      // В случае ошибки выводим ее в консоль
      console.error('Error:', error);
    }
  };


  const handleGroupClick = (week, group) => {
    // Перенаправление на новую страницу с данными выбранной группы
    window.location.href = `/schedule/group/${group}`;
  };
  
// ====================================================================================

  return (
    <div>
      {/* Поле для выбора файла */}
      <input type="file" onChange={handleFileChange} />

      {/* Кнопка для отправки файла на сервер */}
      <button onClick={handleSubmit}>Upload</button>
      
      {/* Если есть расписание, отображаем его */}
      {schedule && (
        <div>

        <h2>Первая неделя</h2>
        {/* Отображение кнопок для каждого ключа первой недели */}

        {Object.keys(schedule['Первая неделя']).map((group, index) => (
          <button key={index} onClick={() => handleGroupClick('Первая неделя', group)}>
            {group}
          </button>
        ))}

        <h2>Вторая неделя</h2>
        {/* Отображение кнопок для каждого ключа второй недели */}

        {Object.keys(schedule['Вторая неделя']).map((group, index) => (
          <button key={index} onClick={() => handleGroupClick('Вторая неделя', group)}>
            {group}
          </button>
        ))}

      </div>
      )}
    </div>
  );
};

// ====================================================================================

export default UploadFile;

// ====================================================================================
