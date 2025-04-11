import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PatientDashboard from './components/PatientDashboard';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <Link to="/">Patient</Link> | 
          <Link to="/admin">Admin</Link>
        </nav>
        <Routes>
          <Route path="/" element={<PatientDashboard />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
