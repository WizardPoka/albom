// TeacherSchedulePage.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import TeacherSchedule from './TeacherSchedule';
import styles from './GroupSchedule/GroupSchedule.module.css';

const TeacherSchedulePage = () => {
    const { teacher } = useParams();
    const [schedule, setSchedule] = useState([]);
    const navigate = useNavigate()

    useEffect(() => {
        const fetchSchedule = async () => {
            const response = await axios.get(`http://localhost:8000/schedule/teacher/${teacher}`);
            setSchedule(response.data);
        };
        fetchSchedule();
    }, [teacher]);

    const handleBack = () => {
        navigate("/groups");
    };

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Расписание преподавателя: {teacher}</h1>
                <button onClick={handleBack}>Назад</button>
            </div>
            <TeacherSchedule schedule={schedule} />
        </div>
    );
};

export default TeacherSchedulePage;
