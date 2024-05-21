import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AdminPanel.module.css';

const AdminPanel = () => {
    const [file, setFile] = useState(null);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState('');
    const [schedule, setSchedule] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');

    useEffect(() => {
        // Fetch groups on mount
        const fetchGroups = async () => {
            try {
                const response = await axios.get('http://localhost:8000/groups');
                setGroups(response.data);
            } catch (error) {
                console.error('Error fetching groups:', error);
            }
        };
        fetchGroups();
    }, []);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setUploadStatus('Файл успешно загружен');
        } catch (error) {
            console.error('Error uploading file:', error);
            setUploadStatus('Ошибка загрузки файла');
        }
    };

    const handleGroupChange = async (e) => {
        const group = e.target.value;
        setSelectedGroup(group);
        try {
            const response = await axios.get(`http://localhost:8000/schedule/group/${group}`);
            setSchedule(response.data);
        } catch (error) {
            console.error('Error fetching schedule:', error);
        }
    };

    const handleChange = (type, index, field, value) => {
        const updatedSchedule = { ...schedule };
        if (updatedSchedule[type]) {
            updatedSchedule[type][index][field] = value;
            setSchedule(updatedSchedule);
        }
    };

    const handleAdd = (type) => {
        const updatedSchedule = { ...schedule };
        updatedSchedule[type].push({});
        setSchedule(updatedSchedule);
    };

    const handleDelete = (type, index) => {
        const updatedSchedule = { ...schedule };
        updatedSchedule[type].splice(index, 1);
        setSchedule(updatedSchedule);
    };

    const handleSave = async () => {
        try {
            await axios.put(`http://localhost:8000/schedule/group/${selectedGroup}`, schedule);
            alert('Расписание сохранено');
        } catch (error) {
            console.error('Error saving schedule:', error);
            alert('Ошибка при сохранении расписания');
        }
    };

    return (
        <div className={styles.adminPanel}>
            <h1>Admin Panel</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            <div>{uploadStatus}</div>
            <select onChange={handleGroupChange} value={selectedGroup}>
                <option value="">Выберите группу</option>
                {groups.map((group, index) => (
                    <option key={index} value={group}>
                        {group}
                    </option>
                ))}
            </select>
            {schedule && (
                <div>
                    <h2>Schedule for {selectedGroup}</h2>
                    {['weeks', 'days', 'lessons'].map((type) => (
                        <div key={type}>
                            <h3>{type}</h3>
                            {schedule[type] && schedule[type].map((item, index) => (
                                <div key={index} className={styles.scheduleItem}>
                                    {Object.keys(item).map((field) => (
                                        <input
                                            key={field}
                                            type="text"
                                            value={item[field]}
                                            onChange={(e) => handleChange(type, index, field, e.target.value)}
                                            placeholder={field}
                                            className={styles.inputField}
                                        />
                                    ))}
                                    <button onClick={() => handleDelete(type, index)}>Delete</button>
                                </div>
                            ))}
                            <button onClick={() => handleAdd(type)}>Add {type.slice(0, -1)}</button>
                        </div>
                    ))}
                    <button onClick={handleSave}>Save</button>
                    <div className={styles.fullSchedule}>
                        <h3>Full Schedule</h3>
                        {schedule && schedule.weeks && schedule.weeks.map((week, weekIndex) => (
    <div key={weekIndex} className={styles.week}>
        <div className={styles.weekTitle}>
            {week.week}
        </div>
        {week.groups && week.groups.map((group, groupIndex) => (
            <div key={groupIndex}>
                {group.days && group.days.map((day, dayIndex) => (
                    <div key={dayIndex} className={styles.day}>
                        <span className={styles.dayNumber}>
                            {day.day}
                        </span>
                        <div>
                            {day.lessons && day.lessons.map((lesson, lessonIndex) => (
                                <li key={lessonIndex} className={styles.lessonTitle}>
                                    <span className={styles.number}>
                                        {lesson.number}
                                    </span>
                                    <span className={styles.time_lesson}>
                                        {lesson.time_lesson}
                                    </span>
                                    <span className={styles.lesson}>
                                        {lesson.lesson}
                                    </span>
                                    <span className={styles.teacher}>
                                        {lesson.teacher}
                                    </span>
                                    <span className={styles.classroom}>
                                        {lesson.classroom}
                                    </span>
                                </li>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        ))}
    </div>
))}

                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminPanel;
