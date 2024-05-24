import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AdminPanel.module.css'; // Assume similar styles as GroupSchedule

const AdminPanel = () => {
    const [file, setFile] = useState(null);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [schedule, setSchedule] = useState(null);
    const [editedSchedule, setEditedSchedule] = useState(null);

    useEffect(() => {
        fetchGroups();
    }, []);

    const fetchGroups = async () => {
        try {
            const response = await axios.get("http://localhost:8000/groups/");
            setGroups(response.data);
        } catch (error) {
            console.error("Error fetching groups", error);
        }
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:8000/upload/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            console.log("File uploaded successfully", response.data);
        } catch (error) {
            console.error("Error uploading file", error);
        }
    };

    const fetchSchedule = async (group) => {
        try {
            const response = await axios.get(`http://localhost:8000/schedule/group/${group}`);
            setSchedule(response.data);
            setEditedSchedule(response.data);
        } catch (error) {
            console.error("Error fetching schedule", error);
        }
    };

    const handleGroupClick = (group) => {
        if (selectedGroup === group) {
            setSelectedGroup(null);
            setSchedule(null);
            setEditedSchedule(null);
        } else {
            setSelectedGroup(group);
            fetchSchedule(group);
        }
    };

    const handleEditChange = (weekIndex, groupIndex, dayIndex, lessonIndex, field, value) => {
        const newSchedule = [...editedSchedule];
        newSchedule[weekIndex].groups[groupIndex].days[dayIndex].lessons[lessonIndex][field] = value;
        setEditedSchedule(newSchedule);
    };

    const handleSave = async () => {
        try {
            const updatedGroups = editedSchedule.flatMap(week => 
                week.groups.map(group => 
                    group.days.map(day => ({
                        group: group.group,
                        day: day.day,
                        lessons: day.lessons
                    }))
                )
            ).flat();
    
            for (const updatedGroup of updatedGroups) {
                await axios.put(`http://localhost:8000/schedule/group/${encodeURIComponent(updatedGroup.group)}/day/${encodeURIComponent(updatedGroup.day)}`, updatedGroup.lessons);
            }
    
            console.log("Schedule updated successfully");
            setSchedule(editedSchedule);
        } catch (error) {
            console.error("Error updating schedule", error);
        }
    };
    

    return (
        <div>
            <h1>Admin Panel</h1>
            <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleUpload}>Upload</button>
            </div>
            <div>
                {groups.map((group) => (
                    <div key={group}>
                        <button onClick={() => handleGroupClick(group)}>{group}</button>
                        {selectedGroup === group && schedule && (
                            <div>
                                {schedule.map((weekSchedule, weekIndex) => (
                                    <div key={weekIndex} className={styles.week}>
                                        <div className={styles.weekTitle}>
                                            {weekSchedule.week}
                                        </div>
                                        {weekSchedule.groups.map((groupSchedule, groupIndex) => (
                                            <div key={`${weekIndex}-${groupIndex}`} className={styles.group}>
                                                {groupSchedule.days.map((daySchedule, dayIndex) => (
                                                    <div key={`${weekIndex}-${groupIndex}-${dayIndex}`} className={styles.day}>
                                                        <span className={styles.dayNumber}>
                                                            {daySchedule.day}
                                                        </span>
                                                        <div>
                                                            {daySchedule.lessons.map((lesson, lessonIndex) => (
                                                                <li key={`${weekIndex}-${groupIndex}-${dayIndex}-${lessonIndex}`} className={styles.lessonTitle}>
                                                                    <span className={styles.number}>
                                                                        {lesson.number}
                                                                    </span>
                                                                    <span className={styles.time_lesson}>
                                                                        {lesson.time_lesson}
                                                                    </span>
                                                                    <input
                                                                        type="text"
                                                                        value={lesson.lesson}
                                                                        onChange={(e) =>
                                                                            handleEditChange(weekIndex, groupIndex, dayIndex, lessonIndex, 'lesson', e.target.value)
                                                                        }
                                                                    />
                                                                    <input
                                                                        type="text"
                                                                        value={lesson.teacher}
                                                                        onChange={(e) =>
                                                                            handleEditChange(weekIndex, groupIndex, dayIndex, lessonIndex, 'teacher', e.target.value)
                                                                        }
                                                                    />
                                                                    <input
                                                                        type="text"
                                                                        value={lesson.classroom}
                                                                        onChange={(e) =>
                                                                            handleEditChange(weekIndex, groupIndex, dayIndex, lessonIndex, 'classroom', e.target.value)
                                                                        }
                                                                    />
                                                                </li>
                                                            ))}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        ))}
                                    </div>
                                ))}
                                <button onClick={handleSave}>Сохранить</button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminPanel;
