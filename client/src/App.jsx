//cd client >> npm start

// ====================================================================================

// App.jsx

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import UploadFile from './UploadFile';
import GroupSchedule from './GroupSchedule';

const App = () => {
  return (
      <Routes>
        <Route path="/" element={<UploadFile />} />
        <Route path="/schedule/group/:group" element={<GroupSchedule />} />

      </Routes>
  );
};

// ====================================================================================

export default App;

// ====================================================================================
