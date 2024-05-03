//cd client >> npm start

// ====================================================================================

// App.jsx

import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import UploadFile from './UploadFile';
import GroupSchedule from './GroupSchedule';
import ListGroups from './ListGroups';

// ====================================================================================

const App = () => {

  const [schedule, setSchedule] = useState(null);

// ====================================================================================

  return (
      <Routes>
        <Route path="/" element={<UploadFile setSchedule={setSchedule} />} />
        <Route path="/groups" element={<ListGroups schedule={schedule} />} /> 
        <Route path="/schedule/group/:group" element={<GroupSchedule />} />

      </Routes>
  );
};

// ====================================================================================

export default App;

// ====================================================================================
