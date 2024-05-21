import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AdminPanel.module.css';

const AdminPanel = () => {
    const [file, setFile] = useState(null);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState("");
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

    const handleGroupChange = (e) => {
        setSelectedGroup(e.target.value);
        fetchSchedule(e.target.value);
    };

    return (
        <div>
            <h1>Admin Panel</h1>
            <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleUpload}>Upload</button>
            </div>
            <div>
                <select onChange={handleGroupChange} value={selectedGroup}>
                    <option value="">Select Group</option>
                    {groups.map((group) => (
                        <option key={group} value={group}>
                            {group}
                        </option>
                    ))}
                </select>
            </div>
            {schedule && (
                <div>
                    <h2>Schedule for {selectedGroup}</h2>
                    <pre>{JSON.stringify(schedule, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default AdminPanel;
