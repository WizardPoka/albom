// TeacherSearch.jsx

import React, { useState } from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import styles from './TeacherSearch.module.css';

const TeacherSearch = ({ setTeacherSchedule }) => {
    const [query, setQuery] = useState('');
    const [teachers, setTeachers] = useState([]);
    const [notFound, setNotFound] = useState(false);  // Добавьте состояние для сообщения "не найдено"
    const navigate = useNavigate()
    
    const handleChange = async (e) => {
        const value = e.target.value;
        setQuery(value);  // Обновление состояния query
        if (value.length > 0) {
            try {
                const response = await axios.get(`http://localhost:8000/search/teachers?query=${value}`);
                setTeachers(response.data);
                setNotFound(response.data.length === 0);  // Установите notFound в зависимости от результатов
            } catch (error) {
                console.error("Error fetching teachers:", error);
            }
        } else {
            setTeachers([]);
            setNotFound(false);
        }
    };

    const handleSelect = async (teacher) => {
        navigate(`/schedule/teacher/${teacher}`);
    };

    return (
        <div className={styles.container}>
            <input
                className={styles.input}
                type="text"
                value={query}
                onChange={handleChange}
                placeholder="Поиск преподавателя..."
            />
            {notFound && <p className={styles.notFound}>Преподаватель не найден</p>}  {/* Сообщение "не найдено" */}
            <ul className={styles.list}>
                {teachers.map((teacher) => (
                    <li className={styles.listItem} key={teacher} onClick={() => handleSelect(teacher)}>
                        {teacher}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TeacherSearch;