import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AdminPanel.module.css'; // Assume similar styles as GroupSchedule
import styles_1 from '../ListGroups/ListGroups.module.css';

const AdminPanel = () => {
    const [file, setFile] = useState(null);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [schedule, setSchedule] = useState(null);

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
        } catch (error) {
            console.error("Error fetching schedule", error);
        }
    };

    const handleGroupClick = (group) => {
        if (selectedGroup === group) {
            setSelectedGroup(null); // Collapse the group if already selected
            setSchedule(null);
        } else {
            setSelectedGroup(group);
            fetchSchedule(group);
        }
    };

    const handleEditLesson = async (lessonId, updatedLessonData) => {
        try {
            const response = await axios.put(`http://localhost:8000/schedule/lesson/${lessonId}`, updatedLessonData);
            console.log("Lesson updated successfully", response.data);
            fetchSchedule(selectedGroup);
        } catch (error) {
            console.error("Error updating lesson", error);
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
                                {schedule.map((weekSchedule, index) => (
                                    <div key={index} className={styles.week}>
                                        <div className={styles.weekTitle}>
                                            {weekSchedule.week}
                                        </div>
                                        {weekSchedule.groups.map((groupSchedule, groupIndex) => (
                                            <div key={groupIndex}>
                                                {groupSchedule.days.map((daySchedule, dayIndex) => (
                                                    <div key={dayIndex} className={styles.day}>
                                                        <span className={styles.dayNumber}>
                                                            {daySchedule.day}
                                                        </span>
                                                        <div>
                                                            {daySchedule.lessons.map((lesson, lessonIndex) => (
                                                                <li key={lessonIndex} className={styles.lessonTitle}>
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
                                                                            handleEditLesson(lesson.lessonId, {
                                                                                ...lesson,
                                                                                lesson: e.target.value
                                                                            })
                                                                        }
                                                                    />
                                                                    <input
                                                                        type="text"
                                                                        value={lesson.teacher}
                                                                        onChange={(e) =>
                                                                            handleEditLesson(lesson.lessonId, {
                                                                                ...lesson,
                                                                                teacher: e.target.value
                                                                            })
                                                                        }
                                                                    />
                                                                    <input
                                                                        type="text"
                                                                        value={lesson.classroom}
                                                                        onChange={(e) =>
                                                                            handleEditLesson(lesson.lessonId, {
                                                                                ...lesson,
                                                                                classroom: e.target.value
                                                                            })
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
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminPanel;
