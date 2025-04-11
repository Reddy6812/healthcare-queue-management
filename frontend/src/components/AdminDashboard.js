import React, { useState } from 'react';
import axios from 'axios';

function AdminDashboard() {
  const [doctorId, setDoctorId] = useState('');
  const [queue, setQueue] = useState([]);

  const handleFetchQueue = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/queue/${doctorId}/`);
      setQueue(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleNotifyNext = async () => {
    try {
      await axios.post('http://localhost:8000/api/notify-next/', { doctor_id: doctorId });
      // Re-fetch queue after updating
      handleFetchQueue();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <label>Doctor ID: </label>
      <input value={doctorId} onChange={e => setDoctorId(e.target.value)} />
      <button onClick={handleFetchQueue}>Fetch Queue</button>
      <button onClick={handleNotifyNext}>Notify Next</button>
      <ul>
        {queue.map(q => (
          <li key={q.id}>{`Position: ${q.position}, Patient: ${q.patient.name}`}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
