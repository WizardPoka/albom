import React from 'react';
import { Link } from 'react-router-dom';

const ListGroups = ({ schedule }) => {
  console.log(schedule);
  if (!schedule) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Список групп</h2>
      {schedule.map((weekData, weekIndex) => (
        <div key={weekIndex}>
          <h2>{weekData.week}</h2>
          {weekData.groups.map((groupData, groupIndex) => (
            
              
              
              <Link to={`/schedule/group/${groupData.group}`}>
                <button>{groupData.group}</button>
              </Link>
            
          ))}
        </div>
      ))}
    </div>
  );
};

export default ListGroups;
