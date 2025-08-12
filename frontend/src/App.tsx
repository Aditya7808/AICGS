import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AuthenticatedWrapper from './components/AuthenticatedWrapper';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import AuthCallback from './pages/AuthCallback';
import MAREAssessment from './pages/MAREAssessment';
import Results from './pages/Results';
import ProgressDashboard from './pages/ProgressDashboard';
import EducationPathwaysPage from './pages/EducationPathwaysPage';
import CASTDemo from './pages/CASTDemo';
import Contact from './pages/Contact';
import './i18n';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AuthenticatedWrapper>
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/auth/callback" element={<AuthCallback />} />
              <Route path="/mare-assessment" element={<MAREAssessment />} />
              <Route path="/results" element={<Results />} />
              <Route path="/progress" element={<ProgressDashboard />} />
              <Route path="/education/:careerIds" element={<EducationPathwaysPage />} />
              <Route path="/cast-demo" element={<CASTDemo />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </AuthenticatedWrapper>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
