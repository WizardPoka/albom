//cd client >> npm start


// ====================================================================================

import React from 'react';
// import './App.css';


import { Routes, Route } from 'react-router-dom';
import UploadFile from './UploadFile';
import GroupSchedule from './GroupSchedule';

const App = () => {
  return (
      <Routes>
        <Route path="/" element={<UploadFile />} />
        <Route path="/schedule/:week/:group" element={<GroupSchedule />} />
      </Routes>
  );
};


// ====================================================================================

// function App() {
//   return (
//     <div>
//       <h1>Загрузка файла на сервер FastAPI</h1>
//       <UploadFile />
//     </div>
//   );
// }

// ====================================================================================

export default App;

// ====================================================================================
