// ListGroups.jsx

// ====================================================================================

import React from 'react';
import { Link } from 'react-router-dom';

import '../../fonts/Golos_Text/GolosText-Regular.ttf'
import styles from './ListGroups.module.css';
// ====================================================================================

const ListGroups = ({ schedule }) => {
  console.log(schedule);
  if (!schedule) {
    return <div>Loading...</div>;
  }

// ====================================================================================
  // Создаем список для хранения всех групп
  const allGroups = [];

  // Проходимся по каждой неделе в расписании
  schedule.forEach(weekData => {
    // Проходимся по каждой группе в текущей неделе
    weekData.groups.forEach(groupData => {
      // Проверяем, нет ли уже такой группы в списке allGroups
      const existingGroup = allGroups.find(group => group.group === groupData.group);
      // Если такой группы нет в списке, добавляем её
      if (!existingGroup) {
        allGroups.push(groupData);
        
      }
    });
  });
  console.log(allGroups)

// ====================================================================================

  return (
    <div className={styles.container}>
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