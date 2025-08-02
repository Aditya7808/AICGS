import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Assessment from './pages/Assessment';
import Results from './pages/Results';
import './i18n';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/assessment" element={<Assessment />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
