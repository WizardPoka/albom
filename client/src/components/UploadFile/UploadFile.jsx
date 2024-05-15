// ====================================================================================

// UploadFile.jsx

import React, { useState  } from 'react';
import axios from 'axios';
import { Link , useNavigate} from 'react-router-dom';

// ====================================================================================



const UploadFile = ({ setSchedule }) => {
  const navigate = useNavigate()
  const [file, setFile] = useState(null); // Состояние для хранения выбранного файла

// ====================================================================================

  // Обработчик изменения файла
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
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
      // Обновляем состояние schedule
      setSchedule(response.data); 
      navigate("/groups")

    } catch (error) {
      // В случае ошибки выводим ее в консоль
      console.error('Error:', error);
    }
  };

// ====================================================================================

  return (
    <div>

      {/* Поле для выбора файла */}
      <input type="file" onChange={handleFileChange} />

      {/* Кнопка для отправки файла на сервер */}
      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
};

// ====================================================================================

export default UploadFile;

// ====================================================================================
