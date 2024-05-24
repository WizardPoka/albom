// TeacherSearch.jsx

import React, { useState } from 'react';
import axios from 'axios';

const TeacherSearch = ({ setTeacherSchedule }) => {
    const [query, setQuery] = useState('');
    const [teachers, setTeachers] = useState([]);

    const handleChange = async (e) => {
        const value = e.target.value;
        setQuery(value);
        if (value.length > 0) {
            const response = await axios.get(`http://localhost:8000/search/teachers?query=${value}`);
            setTeachers(response.data);
        } else {
            setTeachers([]);
        }
    };

    const handleSelect = async (teacher) => {
        const response = await axios.get(`http://localhost:8000/schedule/teacher/${teacher}`);
        setTeacherSchedule(response.data);
        setQuery('');
        setTeachers([]);
    };

    return (
        <div>
            <input
                type="text"
                value={query}
                onChange={handleChange}
                placeholder="Поиск преподавателя..."
            />
            <ul>
                {teachers.map((teacher) => (
                    <li key={teacher} onClick={() => handleSelect(teacher)}>
                        {teacher}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TeacherSearch;
