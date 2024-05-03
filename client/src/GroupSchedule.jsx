// GroupSchedule.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';

const GroupSchedule = () => {
  const { group } = useParams();
  const [schedule, setSchedule] = useState(null);

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
  }, [group]);

  return (
    <div>
      <h1>Расписание </h1>
      <Link to="/">Назад</Link>
      <h2>Расписание для - {group}</h2>
      {schedule ? (
        <pre>{JSON.stringify(schedule, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default GroupSchedule;
