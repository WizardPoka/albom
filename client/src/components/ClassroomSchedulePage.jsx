// ClassroomSchedulePage.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import ClassroomSchedule from './ClassroomSchedule';
import styles from './GroupSchedule/GroupSchedule.module.css';

const ClassroomSchedulePage = () => {
    const { classroom } = useParams();
    const [schedule, setSchedule] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchSchedule = async () => {
            const response = await axios.get(`http://localhost:8000/schedule/classroom/${classroom}`);
            setSchedule(response.data);
        };
        fetchSchedule();
    }, [classroom]);

    const handleBack = () => {
        navigate("/groups");
    };

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Расписание аудитории: {classroom}</h1>
                <button onClick={handleBack}>Назад</button>
            </div>
            <ClassroomSchedule schedule={schedule} />
        </div>
    );
};

export default ClassroomSchedulePage;
