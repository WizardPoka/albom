// ====================================================================================

// ListGroups.jsx

import React from 'react';
import { Link } from 'react-router-dom';

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
    <div>

      <h2>Список групп:</h2>

      {allGroups.map((groupData, index) => (

        <div key={index}>

          <Link to={`/schedule/group/${groupData.group}`}>
            <button>{groupData.group}</button>
          </Link>

        </div>
      ))}

    </div>
  );
};
// ====================================================================================

export default ListGroups;

// ====================================================================================