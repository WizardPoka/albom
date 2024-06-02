// Search.jsx

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styles from './Search.module.css';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState({ teachers: [], classrooms: [] });
    const [notFound, setNotFound] = useState(false);
    const navigate = useNavigate();

    const handleChange = async (e) => {
        const value = e.target.value;
        setQuery(value);
        if (value.length > 0) {
            try {
                const response = await axios.get(`http://localhost:8000/search?query=${value}`);
                setResults(response.data);
                setNotFound(response.data.teachers.length === 0 && response.data.classrooms.length === 0);
            } catch (error) {
                console.error("Error fetching results:", error);
            }
        } else {
            setResults({ teachers: [], classrooms: [] });
            setNotFound(false);
        }
    };

    const handleSelectTeacher = async (teacher) => {
        navigate(`/schedule/teacher/${teacher}`);
    };

    const handleSelectClassroom = async (classroom) => {
        navigate(`/schedule/classroom/${classroom}`);
    };

    return (
        <div className={styles.container}>
            <input
                className={styles.input}
                type="text"
                value={query}
                onChange={handleChange}
                placeholder="Поиск преподавателя или аудитории..."
            />
            {notFound && <p className={styles.notFound}>Преподаватель или аудитория не найдены</p>}
            <div className={styles.resultsContainer}>
                {results.teachers.length > 0 && (
                    <div className={styles.resultsBlock}>
                        <h3>Преподаватели</h3>
                        <ul className={styles.list}>
                            {results.teachers.map((teacher) => (
                                <li className={styles.listItem} key={teacher} onClick={() => handleSelectTeacher(teacher)}>
                                    {teacher}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
                {results.classrooms.length > 0 && (
                    <div className={styles.resultsBlock}>
                        <h3>Аудитории</h3>
                        <ul className={styles.list}>
                            {results.classrooms.map((classroom) => (
                                <li className={styles.listItem} key={classroom} onClick={() => handleSelectClassroom(classroom)}>
                                    {classroom}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Search;

