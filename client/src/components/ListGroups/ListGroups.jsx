// ListGroups.jsx

// ====================================================================================

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import Search from '../Search';
import TeacherSchedule from '../TeacherSchedule';

import '../../fonts/Golos_Text/GolosText-Regular.ttf'
import styles from './ListGroups.module.css';
// ====================================================================================

const ListGroups = ({ schedule }) => {
  const [allGroups, setAllGroups] = useState([]);

  const [teacherSchedule, setTeacherSchedule] = useState([]);

  useEffect(() => {
    if (!schedule) {
      const savedSchedule = localStorage.getItem('schedule');
      if (savedSchedule) {
        schedule = JSON.parse(savedSchedule);
      } else {
        return;
      }
    }

    // Создаем список для хранения всех групп
    const groups = [];

    // Проходимся по каждой неделе в расписании
    schedule.forEach(weekData => {
      // Проходимся по каждой группе в текущей неделе
      weekData.groups.forEach(groupData => {
        // Проверяем, нет ли уже такой группы в списке groups
        const existingGroup = groups.find(group => group.group === groupData.group);
        // Если такой группы нет в списке, добавляем её
        if (!existingGroup) {
          groups.push(groupData);
        }
      });
    });
    setAllGroups(groups);
  }, [schedule]);

  if (!schedule) {
    return <div>Loading...</div>;
  }

// ====================================================================================

  return (
    <div className={styles.container}>

        <div className={styles.listHeader}>
            {/* <div className={styles.title}>Поиск:</div> */}
            <Search setTeacherSchedule={setTeacherSchedule} />
            {/* <TeacherSchedule schedule={teacherSchedule} /> */}
        </div>

      <div className={styles.listHeader}>Список групп:</div>
      <div className={styles.containerGroup}>
      {allGroups.map((groupData, index) => (
        <div key={index} className={styles.groupButton}>
          <Link to={`/schedule/group/${groupData.group}`}>
            <button>{groupData.group}</button>
          </Link>
        </div>
      ))}
      </div>
    </div>
  );
};

// ====================================================================================

export default ListGroups;

// ====================================================================================