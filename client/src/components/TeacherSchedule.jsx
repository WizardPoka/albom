// TeacherSchedule.jsx

import React from 'react';
import styles from './TeacherSchedule.module.css';

const TeacherSchedule = ({ schedule }) => {
    return (
        <div className={styles.scheduleContainer}>
            {schedule.map((item, index) => (
                <div className={styles.scheduleItem} key={index}>
                <h3 className={styles.weekTitle}>{item.week}</h3>
                <p className={styles.scheduleDetails}>Группа: {item.group}</p>
                <p className={styles.scheduleDetails}>День: {item.day}</p>
                <p className={styles.scheduleDetails}>Номер: {item.number}</p>
                <p className={styles.scheduleDetails}>Время: {item.time_lesson}</p>
                <p className={styles.scheduleDetails}>Предмет: {item.lesson}</p>
                <p className={styles.scheduleDetails}>Кабинет: {item.classroom}</p>
            </div>
            ))}
        </div>
    );
};

export default TeacherSchedule;
