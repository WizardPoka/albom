// UploadFile.jsx

// ====================================================================================

import React, { useState  } from 'react';
import axios from 'axios';
import { Link , useNavigate} from 'react-router-dom';

import '../../fonts/Golos_Text/GolosText-Regular.ttf'
import styles from './UploadFile.module.css';
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
      const scheduleData = response.data;
      setSchedule(scheduleData); 
      localStorage.setItem('schedule', JSON.stringify(scheduleData)); // Save to local storage
      navigate("/groups");

    } catch (error) {
      // В случае ошибки выводим ее в консоль
      console.error('Error:', error);
    }
  };

// ====================================================================================

  return (
    <div className={styles.container}>
      <div className={styles.uploadFileButton}>
      {/* Поле для выбора файла */}
      <input type="file" onChange={handleFileChange} />

      {/* Кнопка для отправки файла на сервер */}
      
      <button onClick={handleSubmit}>Загрузить расписание</button>
    
      </div>
    </div>
  );
};

// ====================================================================================

export default UploadFile;

// ====================================================================================
