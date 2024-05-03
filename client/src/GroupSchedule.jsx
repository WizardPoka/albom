// GroupSchedule.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const GroupSchedule = () => {
  const { week, group } = useParams()
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/schedule/${week}/${group}`);

        setSchedule(response.data);
      } catch (error) {
        console.error('Error fetching schedule:', error);
      }
    };

    fetchSchedule();
  }, [week, group]);

  return (
    <div>
      <h1>Get Group Schedule</h1>
      <h2>{group} Schedule for {week}</h2>
      {schedule ? (
        <pre>{JSON.stringify(schedule, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default GroupSchedule;
