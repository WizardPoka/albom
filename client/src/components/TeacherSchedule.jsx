// TeacherSchedule.jsx

import React from 'react';

const TeacherSchedule = ({ schedule }) => {
    return (
        <div>
            {schedule.map((item, index) => (
                <div key={index}>
                    <h3>{item.week}</h3>
                    <p>Группа: {item.group}</p>
                    <p>День: {item.day}</p>
                    <p>Номер: {item.number}</p>
                    <p>Время: {item.time_lesson}</p>
                    <p>Предмет: {item.lesson}</p>
                    <p>Кабинет: {item.classroom}</p>
                </div>
            ))}
        </div>
    );
};

export default TeacherSchedule;
