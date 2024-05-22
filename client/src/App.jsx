//cd client >> npm start

// App.jsx

// ====================================================================================

import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import UploadFile from './components/UploadFile/UploadFile';
import GroupSchedule from './components/GroupSchedule/GroupSchedule';
import ListGroups from './components/ListGroups/ListGroups';
import AdminPanel from './components/AdminPanel/AdminPanel';
// ====================================================================================

const App = () => {
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    const savedSchedule = localStorage.getItem('schedule');
    if (savedSchedule) {
      setSchedule(JSON.parse(savedSchedule));
    }
  }, []);

// ====================================================================================

  return (
      <Routes>
        <Route path="/" element={<UploadFile setSchedule={setSchedule} />} />
        <Route path="/groups" element={<ListGroups schedule={schedule} />} /> 
        <Route path="/schedule/group/:group" element={<GroupSchedule />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
  );
};

// ====================================================================================

export default App;

// ====================================================================================
 