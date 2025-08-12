import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import EducationPathways from '../components/EducationPathways';
import Loading from '../components/Loading';
import Button from '../components/Button';
import { GraduationCap, ArrowLeft } from 'lucide-react';

const EducationPathwaysPage: React.FC = () => {
  const { careerIds } = useParams<{ careerIds: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  const [parsedCareerIds, setParsedCareerIds] = useState<number[]>([]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (careerIds) {
      try {
        const ids = careerIds.split(',').map(id => parseInt(id.trim(), 10)).filter(id => !isNaN(id));
        setParsedCareerIds(ids);
      } catch (error) {
        console.error('Error parsing career IDs:', error);
        navigate('/results');
      }
    } else {
      // If no career IDs provided, redirect to MARE assessment
      navigate('/mare-assessment');
    }
  }, [careerIds, isAuthenticated, navigate]);

  if (!isAuthenticated) {
    return <Loading />;
  }

  if (parsedCareerIds.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center py-12">
            <GraduationCap className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Education Pathways</h1>
            <p className="text-gray-600 mb-6">
              Please complete the MARE AI assessment to view personalized education pathways.
            </p>
            <Button onClick={() => navigate('/mare-assessment')}>
              Take MARE Assessment
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate('/results')}
                className="flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Results
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Education Pathways</h1>
                <p className="text-gray-600 mt-1">
                  Explore courses, institutions, and admission processes for your career goals
                </p>
              </div>
            </div>
            
            {user && (
              <div className="text-right">
                <div className="text-sm text-gray-600">Welcome back,</div>
                <div className="font-medium text-gray-900">{user.full_name || user.email}</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <EducationPathways
          careerIds={parsedCareerIds}
          userProfile={{
            currentEducation: '12th', // This would come from user profile
            budget: 'medium',
            location: 'India'
          }}
        />
      </div>
    </div>
  );
};

export default EducationPathwaysPage;
