import React, { useState } from 'react';
import axios from 'axios';

function PatientDashboard() {
  const [doctorId, setDoctorId] = useState('');
  const [patientId, setPatientId] = useState('');
  const [queueResponse, setQueueResponse] = useState(null);

  const handleEnqueue = async () => {
    try {
      const res = await axios.post('http://localhost:8000/api/enqueue/', {
        doctor_id: doctorId,
        patient_id: patientId,
      });
      setQueueResponse(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Patient Dashboard</h2>
      <label>Doctor ID: </label>
      <input value={doctorId} onChange={e => setDoctorId(e.target.value)} />
      <br />
      <label>Patient ID: </label>
      <input value={patientId} onChange={e => setPatientId(e.target.value)} />
      <br />
      <button onClick={handleEnqueue}>Enqueue</button>
      <br />
      {queueResponse && <pre>{JSON.stringify(queueResponse, null, 2)}</pre>}
    </div>
  );
}

export default PatientDashboard;
