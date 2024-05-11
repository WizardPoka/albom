// ====================================================================================

// GroupSchedule.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';


import './fonts/Golos_Text/GolosText-Regular.ttf'
import styles from './GroupSchedule.module.css';
import imageUrl from'./image/gradient.png'
// ====================================================================================

const GroupSchedule = () => {
  const { group } = useParams();
  const [schedule, setSchedule] = useState(null);
  
// ====================================================================================

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/schedule/group/${group}`);
        setSchedule(response.data);
      } catch (error) {
        console.error('Error fetching schedule:', error);
      }
    };

    fetchSchedule();
  }, [group], console.log(group));

// ====================================================================================

  return (
    <div>
    <div className={styles.backgroundColor}>
    <div className={styles.container}> 
        <div className={styles.header}>
          <h1 className={styles.title}>Расписание</h1>
          <Link to="/groups">Назад</Link>
        </div>
        <h2>{group}</h2>
        {schedule ? (
          <div>
            {schedule.map((weekSchedule, index) => (
              <div key={index} className={styles.week}>

                <div className={styles.weekTitle}>
                  {index === 0 ? 'Первая неделя' : 'Вторая неделя'}
                </div>
                {weekSchedule.map((daySchedule, dayIndex) => (

                  <div key={dayIndex} className={styles.day}>

                    <span className={styles.dayNumber}>
                      {daySchedule.day}
                    </span>

                    <div>
                      {daySchedule.lessons.map((lesson, lessonIndex) => (
                        <li key={lessonIndex} className={styles.lessonTitle}>

                          

                          <span className={styles.number}>
                            {lesson.number}
                          </span>
                          <span className={styles.lesson}>
                            {lesson.lesson}
                          </span>
                          <span className={styles.teacher}>
                            {lesson.teacher}
                          </span>
                          <span className={styles.classroom}>
                            {lesson.classroom}
                          </span>
                        </li>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
    </div>
  );
};


// ====================================================================================

export default GroupSchedule;

// ====================================================================================