// ClassroomSchedule.jsx

import React from 'react';
import styles from './TeacherClassroomSchedule.module.css';

const groupBy = (array, key) => {
    return array.reduce((result, currentValue) => {
        (result[currentValue[key]] = result[currentValue[key]] || []).push(currentValue);
        return result;
    }, {});
};

const ClassroomSchedule = ({ schedule }) => {
    const weeks = groupBy(schedule, 'week');

    return (
        <div className={styles.scheduleContainer}>
            {Object.keys(weeks).map(week => {
                const groups = groupBy(weeks[week], 'group');
                return (
                    <div className={styles.scheduleItem} key={week}>
                        <h3 className={styles.weekTitle}>{week}</h3>
                        {Object.keys(groups).map(group => {
                            const days = groupBy(groups[group], 'day');
                            return (
                                <div key={group} className={styles.groupBlock}>
                                    <h4 className={styles.groupTitle}>Группа: {group}</h4>
                                    {Object.keys(days).map(day => (
                                        <div key={day} className={styles.dayBlock}>
                                            <h5 className={styles.dayTitle}>День: {day}</h5>
                                            {days[day].map((item, index) => (
                                                <div key={index} className={styles.scheduleDetailsContainer}>
                                                    <div className={styles.scheduleDetailBox}>
                                                        <p className={styles.scheduleDetails}>Номер: {item.number}</p>
                                                        <p className={styles.scheduleDetails}>Время: {item.time_lesson}</p>
                                                        <p className={styles.scheduleDetails}>Предмет: {item.lesson}</p>
                                                        <p className={styles.scheduleDetails}>Кабинет: {item.classroom}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    ))}
                                </div>
                            );
                        })}
                    </div>
                );
            })}
        </div>
    );
};

export default ClassroomSchedule;

