// ====================================================================================

// ListGroups.jsx

import React from 'react';
import { Link } from 'react-router-dom';

// ====================================================================================

const ListGroups = ({ schedule }) => {

  return (
    <div>
      <h2>Список групп</h2>
      {schedule && (
        <div>
          <h2>Первая неделя</h2>
          {Object.keys(schedule['Первая неделя']).map((group, index) => (
            <Link key={index} to={`/schedule/group/${group}`}>
              <button>{group}</button>
            </Link>
          ))}

          <h2>Вторая неделя</h2>
          {Object.keys(schedule['Вторая неделя']).map((group, index) => (
            <Link key={index} to={`/schedule/group/${group}`}>
              <button>{group}</button>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

// ====================================================================================

export default ListGroups;

// ====================================================================================