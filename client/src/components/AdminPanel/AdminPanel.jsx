import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AdminPanel.module.css';

const AdminPanel = () => {
  const [file, setFile] = useState(null);
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await axios.get('http://localhost:8000/groups/');
      setGroups(response.data);
    } catch (error) {
      console.error('Error fetching groups:', error);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/upload/', formData);
      alert('File uploaded successfully');
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleGroupClick = async (group) => {
    try {
      const response = await axios.get(`http://localhost:8000/schedule/group/${group}`);
      setSelectedGroup(response.data);
      setEditData(response.data);  // Сохраняем данные для редактирования
    } catch (error) {
      console.error('Error fetching group schedule:', error);
    }
  };

  const handleEditClick = () => {
    setIsEditing(true);
    
  };

  const handleSaveClick = async () => {
    try {
        const payload = JSON.stringify(editData);
        await axios.post('http://localhost:8000/save_schedule', payload, {
            headers: {
            'Content-Type': 'application/json'
            }
        });
      
        setIsEditing(false);
        fetchGroups();
    } catch (error) {
        console.error('Error saving schedule:', error);
    }
  };

  const handleInputChange = (dayIndex, lessonIndex, field, value) => {
    const newEditData = { ...editData };
    newEditData.days[dayIndex].lessons[lessonIndex][field] = value;
    setEditData(newEditData);
  };

  const renderGroups = () => (
    <div>
      {groups.map((group, index) => (
        <button key={index} onClick={() => handleGroupClick(group)} className={styles.groupButton}>
          {group}
        </button>
      ))}
    </div>
  );

  const renderGroupDetails = () => {
    if (!selectedGroup) return null;
  
    return (
      <div>
        <h2>{selectedGroup.group}</h2>
        <button onClick={handleEditClick} className={styles.editButton}>Edit</button>
        <div>
          {selectedGroup.days && selectedGroup.days.map((day, dayIndex) => (
            <div key={dayIndex}>
              <h3>{day.day}</h3>
              {day.lessons.map((lesson, lessonIndex) => (
                <div key={lessonIndex} className={styles.lesson}>
                  <span>{lesson.number} - {lesson.lesson}</span>
                  {isEditing && (
                    <div className={styles.editFields}>
                      <input
                        type="text"
                        value={editData.groups[0].days[dayIndex].lessons[lessonIndex].lesson}
                        onChange={(e) => handleInputChange(0, dayIndex, lessonIndex, 'lesson', e.target.value)}
                      />
                      <input
                        type="text"
                        value={editData.groups[0].days[dayIndex].lessons[lessonIndex].teacher}
                        onChange={(e) => handleInputChange(0, dayIndex, lessonIndex, 'teacher', e.target.value)}
                      />
                      <input
                        type="text"
                        value={editData.groups[0].days[dayIndex].lessons[lessonIndex].classroom}
                        onChange={(e) => handleInputChange(0, dayIndex, lessonIndex, 'classroom', e.target.value)}
                      />
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
        {isEditing && (
          <button onClick={handleSaveClick} className={styles.saveButton}>Save</button>
        )}
      </div>
    );
  };
  

  return (
    <div className={styles.adminPanel}>
      <h1>Admin Panel</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} className={styles.uploadButton}>Upload</button>
      {renderGroups()}
      {renderGroupDetails()}
    </div>
  );
};

export default AdminPanel;
