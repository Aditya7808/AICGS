import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import AssessmentForm from '../components/AssessmentForm';

const Assessment: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [results, setResults] = useState(null);

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleResults = (data: any) => {
    setResults(data);
    // Store results in localStorage for the Results page
    localStorage.setItem('careerResults', JSON.stringify(data));
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen">
      <AssessmentForm onResults={handleResults} />
    </div>
  );
};

export default Assessment;
