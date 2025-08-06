import React, { useState, useEffect } from 'react';
import {
  GraduationCap, MapPin, DollarSign, TrendingUp,
  Clock, Award, BookOpen, ExternalLink, Filter,
  ChevronDown, ChevronUp, Star, Building, FileText,
  Target, CheckCircle, Trophy
} from 'lucide-react';
import { 
  educationAPI, 
  EducationPathway, 
  InstitutionPathway, 
  Course,
  AdmissionProcess,
  EntranceExamInfo
} from '../services/api';
import Loading from './Loading';
import Button from './Button';

interface EducationPathwaysProps {
  careerIds: number[];
  userProfile?: {
    currentEducation: string;
    budget: string;
    location: string;
  };
}

const EducationPathways: React.FC<EducationPathwaysProps> = ({ 
  careerIds,
  userProfile 
}) => {
  const [pathways, setPathways] = useState<EducationPathway[]>([]);
  const [selectedPathway, setSelectedPathway] = useState<EducationPathway | null>(null);
  const [institutions, setInstitutions] = useState<InstitutionPathway[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [admissionProcesses, setAdmissionProcesses] = useState<AdmissionProcess[]>([]);
  const [entranceExams, setEntranceExams] = useState<EntranceExamInfo[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // UI state
  const [activeTab, setActiveTab] = useState<'overview' | 'courses' | 'institutions' | 'admission' | 'exams'>('overview');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedInstitution, setSelectedInstitution] = useState<InstitutionPathway | null>(null);
  
  // Filters
  const [filters, setFilters] = useState({
    education_level: '',
    budget_max: '',
    pathway_type: '',
    location_filter: '',
    ranking_min: ''
  });

  // Utility functions
  const formatCurrency = (amount?: number) => {
    if (!amount) return 'N/A';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatDuration = (months?: number) => {
    if (!months) return 'N/A';
    if (months < 12) return `${months} months`;
    const years = Math.floor(months / 12);
    const remainingMonths = months % 12;
    return remainingMonths > 0 ? `${years}.${Math.round(remainingMonths * 10 / 12)} years` : `${years} years`;
  };

  const getDifficultyColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case 'beginner': return 'text-green-600 bg-green-100';
      case 'intermediate': return 'text-yellow-600 bg-yellow-100';
      case 'advanced': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getPathwayTypeIcon = (type: string) => {
    switch (type) {
      case 'degree': return <GraduationCap className="w-5 h-5" />;
      case 'bootcamp': return <Clock className="w-5 h-5" />;
      case 'certification': return <Award className="w-5 h-5" />;
      case 'diploma': return <BookOpen className="w-5 h-5" />;
      default: return <FileText className="w-5 h-5" />;
    }
  };

  useEffect(() => {
    if (careerIds.length > 0) {
      loadPathways();
    }
  }, [careerIds]);

  useEffect(() => {
    if (selectedPathway) {
      loadPathwayDetails();
    }
  }, [selectedPathway]);

  const loadPathways = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // For multiple careers, get pathways for the first one (could be enhanced to merge)
      const pathwaysData = await educationAPI.getPathways(careerIds[0], {
        education_level: filters.education_level || undefined,
        budget_max: filters.budget_max ? parseFloat(filters.budget_max) : undefined,
        pathway_type: filters.pathway_type || undefined
      });
      
      setPathways(pathwaysData);
      
      // Auto-select first pathway
      if (pathwaysData.length > 0) {
        setSelectedPathway(pathwaysData[0]);
      }
      
    } catch (err) {
      setError('Failed to load education pathways');
      console.error('Error loading pathways:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadPathwayDetails = async () => {
    if (!selectedPathway) return;
    
    try {
      // Load courses, institutions, and related data
      const [coursesData, institutionsData] = await Promise.all([
        educationAPI.getPathwayCourses(selectedPathway.id),
        educationAPI.getPathwayInstitutions(selectedPathway.id, {
          location_filter: filters.location_filter || undefined,
          ranking_min: filters.ranking_min ? parseInt(filters.ranking_min) : undefined
        })
      ]);
      
      setCourses(coursesData);
      setInstitutions(institutionsData);
      
      // Load entrance exams info if available
      if (selectedPathway.entrance_exams && selectedPathway.entrance_exams.length > 0) {
        const examsData = await educationAPI.getEntranceExamsInfo(selectedPathway.entrance_exams);
        setEntranceExams(examsData);
      }
      
    } catch (err) {
      console.error('Error loading pathway details:', err);
    }
  };

  const loadAdmissionProcesses = async (institutionId: number) => {
    try {
      const processesData = await educationAPI.getAdmissionProcesses(
        institutionId,
        selectedPathway?.id
      );
      setAdmissionProcesses(processesData);
    } catch (err) {
      console.error('Error loading admission processes:', err);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div className="text-red-600 mb-2">⚠️ {error}</div>
        <Button onClick={loadPathways} variant="outline" size="sm">
          Try Again
        </Button>
      </div>
    );
  }

  if (pathways.length === 0) {
    return (
      <div className="text-center py-12">
        <GraduationCap className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <div className="text-gray-600 text-lg mb-2">No Education Pathways Found</div>
        <div className="text-gray-500">Try adjusting your filters or check back later.</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              🎯 Education Pathways
            </h2>
            <p className="text-gray-600">
              Discover courses, institutions, and admission processes tailored to your career goals
            </p>
          </div>
          <Button
            onClick={() => setShowFilters(!showFilters)}
            variant="outline"
            size="sm"
            className="flex items-center gap-2"
          >
            <Filter className="w-4 h-4" />
            Filters
            {showFilters ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </Button>
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-5 gap-4 p-4 bg-white rounded-lg border">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Education Level
              </label>
              <select
                value={filters.education_level}
                onChange={(e) => setFilters(prev => ({ ...prev, education_level: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Levels</option>
                <option value="10th">After 10th</option>
                <option value="12th">After 12th</option>
                <option value="Graduate">After Graduation</option>
                <option value="Postgraduate">After Post-graduation</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Budget (₹)
              </label>
              <input
                type="number"
                value={filters.budget_max}
                onChange={(e) => setFilters(prev => ({ ...prev, budget_max: e.target.value }))}
                placeholder="e.g., 500000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Pathway Type
              </label>
              <select
                value={filters.pathway_type}
                onChange={(e) => setFilters(prev => ({ ...prev, pathway_type: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Types</option>
                <option value="degree">Degree</option>
                <option value="bootcamp">Bootcamp</option>
                <option value="certification">Certification</option>
                <option value="diploma">Diploma</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location
              </label>
              <input
                type="text"
                value={filters.location_filter}
                onChange={(e) => setFilters(prev => ({ ...prev, location_filter: e.target.value }))}
                placeholder="e.g., Delhi, Mumbai"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex items-end">
              <Button onClick={loadPathways} className="w-full">
                Apply Filters
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Pathways Selection */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {pathways.map((pathway) => (
          <div
            key={pathway.id}
            onClick={() => setSelectedPathway(pathway)}
            className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
              selectedPathway?.id === pathway.id
                ? 'border-blue-500 bg-blue-50 shadow-lg'
                : 'border-gray-200 bg-white hover:border-blue-300 hover:shadow-md'
            }`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${selectedPathway?.id === pathway.id ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'}`}>
                  {getPathwayTypeIcon(pathway.pathway_type)}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 line-clamp-2">
                    {pathway.pathway_name}
                  </h3>
                  <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(pathway.difficulty_level)}`}>
                    {pathway.difficulty_level || 'N/A'}
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Clock className="w-4 h-4" />
                {formatDuration(pathway.duration_months)}
              </div>
              
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <DollarSign className="w-4 h-4" />
                {formatCurrency(pathway.estimated_cost_min)} - {formatCurrency(pathway.estimated_cost_max)}
              </div>

              <div className="flex items-center gap-2 text-sm text-gray-600">
                <TrendingUp className="w-4 h-4" />
                {pathway.average_placement_rate}% placement rate
              </div>

              <div className="flex items-center gap-1">
                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="text-sm font-medium">{pathway.popularity_score.toFixed(1)}</span>
                <span className="text-xs text-gray-500">popularity</span>
              </div>
            </div>

            {pathway.description && (
              <p className="text-sm text-gray-600 mt-3 line-clamp-2">
                {pathway.description}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Selected Pathway Details */}
      {selectedPathway && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">
          {/* Tabs */}
          <div className="border-b border-gray-200">
            <div className="flex space-x-8 px-6">
              {[
                { id: 'overview', label: 'Overview', icon: <FileText className="w-4 h-4" /> },
                { id: 'courses', label: 'Courses', icon: <BookOpen className="w-4 h-4" /> },
                { id: 'institutions', label: 'Institutions', icon: <Building className="w-4 h-4" /> },
                { id: 'admission', label: 'Admission', icon: <Target className="w-4 h-4" /> },
                { id: 'exams', label: 'Entrance Exams', icon: <Award className="w-4 h-4" /> }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <PathwayOverview pathway={selectedPathway} formatCurrency={formatCurrency} formatDuration={formatDuration} />
            )}
            {activeTab === 'courses' && (
              <CoursesList courses={courses} />
            )}
            {activeTab === 'institutions' && (
              <InstitutionsList
                institutions={institutions}
                onSelectInstitution={(inst) => {
                  setSelectedInstitution(inst);
                  loadAdmissionProcesses(inst.institution.id);
                }}
                formatCurrency={formatCurrency}
              />
            )}
            {activeTab === 'admission' && (
              <AdmissionProcesses
                processes={admissionProcesses}
                selectedInstitution={selectedInstitution}
              />
            )}
            {activeTab === 'exams' && (
              <EntranceExamsList exams={entranceExams} getDifficultyColor={getDifficultyColor} />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Sub-components for different tabs
const PathwayOverview: React.FC<{ 
  pathway: EducationPathway;
  formatCurrency: (amount?: number) => string;
  formatDuration: (months?: number) => string;
}> = ({ pathway, formatCurrency, formatDuration }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-xl font-semibold text-gray-900 mb-3">
        {pathway.pathway_name}
      </h3>
      <p className="text-gray-600 leading-relaxed">
        {pathway.description}
      </p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div className="bg-blue-50 p-4 rounded-lg">
        <div className="text-blue-600 text-2xl font-bold">
          {formatDuration(pathway.duration_months)}
        </div>
        <div className="text-sm text-blue-700">Duration</div>
      </div>
      
      <div className="bg-green-50 p-4 rounded-lg">
        <div className="text-green-600 text-2xl font-bold">
          {pathway.average_placement_rate}%
        </div>
        <div className="text-sm text-green-700">Placement Rate</div>
      </div>
      
      <div className="bg-purple-50 p-4 rounded-lg">
        <div className="text-purple-600 text-2xl font-bold">
          ₹{pathway.average_starting_salary ? (pathway.average_starting_salary / 100000).toFixed(1) : 'N/A'}L
        </div>
        <div className="text-sm text-purple-700">Starting Salary</div>
      </div>
      
      <div className="bg-orange-50 p-4 rounded-lg">
        <div className="text-orange-600 text-2xl font-bold">
          {pathway.min_percentage || 'N/A'}%
        </div>
        <div className="text-sm text-orange-700">Min. Percentage</div>
      </div>
    </div>

    {/* Requirements */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="space-y-4">
        <h4 className="font-semibold text-gray-900">Requirements</h4>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            <span className="text-sm">Education: {pathway.min_education_level}</span>
          </div>
          {pathway.required_subjects && (
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
              <div className="text-sm">
                <span>Subjects: </span>
                {pathway.required_subjects.join(', ')}
              </div>
            </div>
          )}
          {pathway.entrance_exams && pathway.entrance_exams.length > 0 && (
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
              <div className="text-sm">
                <span>Entrance Exams: </span>
                {pathway.entrance_exams.join(', ')}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="space-y-4">
        <h4 className="font-semibold text-gray-900">Financial Information</h4>
        <div className="space-y-2">
          <div className="text-sm">
            <span className="font-medium">Cost Range: </span>
            {formatCurrency(pathway.estimated_cost_min)} - {formatCurrency(pathway.estimated_cost_max)}
          </div>
          {pathway.financial_aid_available && (
            <div className="flex items-center gap-2 text-sm text-green-600">
              <CheckCircle className="w-4 h-4" />
              Financial aid available
            </div>
          )}
          {pathway.scholarship_opportunities && (
            <div className="text-sm">
              <span className="font-medium">Scholarships: </span>
              {pathway.scholarship_opportunities.join(', ')}
            </div>
          )}
        </div>
      </div>
    </div>

    {/* Top Companies */}
    {pathway.top_recruiting_companies && (
      <div>
        <h4 className="font-semibold text-gray-900 mb-3">Top Recruiting Companies</h4>
        <div className="flex flex-wrap gap-2">
          {pathway.top_recruiting_companies.map((company, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
            >
              {company}
            </span>
          ))}
        </div>
      </div>
    )}
  </div>
);

const CoursesList: React.FC<{ courses: Course[] }> = ({ courses }) => {
  if (courses.length === 0) {
    return (
      <div className="text-center py-8">
        <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-600">No course information available</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Course Curriculum</h3>
      
      <div className="grid gap-4">
        {courses.map((course) => (
          <div key={course.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h4 className="font-semibold text-gray-900">
                  {course.name}
                  {course.code && <span className="text-gray-500 ml-2">({course.code})</span>}
                </h4>
                {course.description && (
                  <p className="text-sm text-gray-600 mt-1">{course.description}</p>
                )}
              </div>
              <div className="text-right text-sm text-gray-500">
                {course.semester && <div>Semester {course.semester}</div>}
                {course.credits && <div>{course.credits} credits</div>}
              </div>
            </div>

            {course.topics_covered && (
              <div className="mb-3">
                <span className="text-sm font-medium text-gray-700">Topics: </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {course.topics_covered.map((topic, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {course.skills_gained && (
              <div>
                <span className="text-sm font-medium text-gray-700">Skills Gained: </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {course.skills_gained.map((skill, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-green-50 text-green-700 rounded text-xs"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

const InstitutionsList: React.FC<{
  institutions: InstitutionPathway[];
  onSelectInstitution: (institution: InstitutionPathway) => void;
  formatCurrency: (amount?: number) => string;
}> = ({ institutions, onSelectInstitution, formatCurrency }) => {
  if (institutions.length === 0) {
    return (
      <div className="text-center py-8">
        <Building className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-600">No institutions found</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Top Institutions</h3>
      
      <div className="grid gap-4">
        {institutions.map((instPathway) => (
          <div
            key={instPathway.id}
            className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => onSelectInstitution(instPathway)}
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h4 className="font-semibold text-lg text-gray-900">
                  {instPathway.institution.name}
                </h4>
                <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-4 h-4" />
                    {instPathway.institution.city}, {instPathway.institution.state}
                  </div>
                  {instPathway.institution.ranking_national && (
                    <div className="flex items-center gap-1">
                      <Trophy className="w-4 h-4" />
                      Rank #{instPathway.institution.ranking_national}
                    </div>
                  )}
                </div>
              </div>
              {instPathway.institution.website && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    window.open(instPathway.institution.website, '_blank');
                  }}
                  className="flex items-center gap-1"
                >
                  <ExternalLink className="w-3 h-3" />
                  Visit
                </Button>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <div className="text-sm text-gray-600">Annual Fees</div>
                <div className="font-semibold text-gray-900">
                  {formatCurrency(instPathway.fees_per_year)}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Duration</div>
                <div className="font-semibold text-gray-900">
                  {instPathway.duration_years} years
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Seats</div>
                <div className="font-semibold text-gray-900">
                  {instPathway.seats_available || 'N/A'}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Placement Rate</div>
                <div className="font-semibold text-gray-900">
                  {instPathway.placement_statistics?.placement_rate || 'N/A'}%
                </div>
              </div>
            </div>

            {instPathway.entrance_exams_accepted && instPathway.entrance_exams_accepted.length > 0 && (
              <div>
                <div className="text-sm text-gray-600 mb-1">Entrance Exams Accepted:</div>
                <div className="flex flex-wrap gap-1">
                  {instPathway.entrance_exams_accepted.map((exam, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-yellow-50 text-yellow-700 rounded text-xs"
                    >
                      {exam}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {instPathway.institution.facilities && (
              <div className="mt-3">
                <div className="text-sm text-gray-600 mb-1">Facilities:</div>
                <div className="flex flex-wrap gap-1">
                  {instPathway.institution.facilities.map((facility, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-50 text-gray-700 rounded text-xs"
                    >
                      {facility}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

const AdmissionProcesses: React.FC<{
  processes: AdmissionProcess[];
  selectedInstitution: InstitutionPathway | null;
}> = ({ processes, selectedInstitution }) => {
  if (!selectedInstitution) {
    return (
      <div className="text-center py-8">
        <Target className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-600">Select an institution to view admission processes</div>
      </div>
    );
  }

  if (processes.length === 0) {
    return (
      <div className="text-center py-8">
        <FileText className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-600">No admission process information available</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">
        Admission Process - {selectedInstitution.institution.name}
      </h3>
      
      {processes.map((process) => (
        <div key={process.id} className="border border-gray-200 rounded-lg p-6">
          <h4 className="font-semibold text-gray-900 mb-4">{process.process_name}</h4>
          
          {/* Timeline */}
          {(process.application_start_date || process.exam_dates) && (
            <div className="mb-4">
              <h5 className="font-medium text-gray-800 mb-2">Important Dates</h5>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                {process.application_start_date && (
                  <div>
                    <span className="text-gray-600">Application Start:</span>
                    <div className="font-medium">{process.application_start_date}</div>
                  </div>
                )}
                {process.application_end_date && (
                  <div>
                    <span className="text-gray-600">Application End:</span>
                    <div className="font-medium">{process.application_end_date}</div>
                  </div>
                )}
                {process.exam_dates && process.exam_dates.length > 0 && (
                  <div>
                    <span className="text-gray-600">Exam Dates:</span>
                    <div className="font-medium">{process.exam_dates.join(', ')}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Eligibility */}
          {process.eligibility_criteria && (
            <div className="mb-4">
              <h5 className="font-medium text-gray-800 mb-2">Eligibility Criteria</h5>
              <div className="text-sm text-gray-600">
                {JSON.stringify(process.eligibility_criteria)}
              </div>
            </div>
          )}

          {/* Preparation */}
          {process.preparation_resources && (
            <div className="mb-4">
              <h5 className="font-medium text-gray-800 mb-2">Preparation Resources</h5>
              <div className="text-sm text-gray-600">
                {JSON.stringify(process.preparation_resources)}
              </div>
            </div>
          )}

          {/* Success Tips */}
          {process.success_tips && process.success_tips.length > 0 && (
            <div>
              <h5 className="font-medium text-gray-800 mb-2">Success Tips</h5>
              <ul className="text-sm text-gray-600 space-y-1">
                {process.success_tips.map((tip, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

const EntranceExamsList: React.FC<{ 
  exams: EntranceExamInfo[];
  getDifficultyColor: (difficulty?: string) => string;
}> = ({ exams, getDifficultyColor }) => {
  if (exams.length === 0) {
    return (
      <div className="text-center py-8">
        <Award className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-600">No entrance exam information available</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Entrance Exams</h3>
      
      {exams.map((exam) => (
        <div key={exam.name} className="border border-gray-200 rounded-lg p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h4 className="font-semibold text-lg text-gray-900">{exam.name}</h4>
              <p className="text-gray-600">{exam.full_name}</p>
              <div className="text-sm text-gray-500 mt-1">
                Conducted by: {exam.conducting_authority}
              </div>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(exam.difficulty_level)}`}>
              {exam.difficulty_level}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            <div>
              <div className="text-sm text-gray-600">Duration</div>
              <div className="font-medium">{exam.duration}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Total Marks</div>
              <div className="font-medium">{exam.total_marks}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Application Fee</div>
              <div className="font-medium">₹{exam.application_fee}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Exam Dates</div>
              <div className="font-medium">{exam.exam_dates.join(', ')}</div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h5 className="font-medium text-gray-800 mb-2">Subjects</h5>
              <div className="flex flex-wrap gap-1">
                {exam.subjects.map((subject, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-sm"
                  >
                    {subject}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h5 className="font-medium text-gray-800 mb-2">Accepted By</h5>
              <div className="flex flex-wrap gap-1">
                {exam.accepted_by.map((institution, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-green-50 text-green-700 rounded text-sm"
                  >
                    {institution}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {exam.preparation_tips && (
            <div className="mt-4">
              <h5 className="font-medium text-gray-800 mb-2">Preparation Tips</h5>
              <ul className="text-sm text-gray-600 space-y-1">
                {exam.preparation_tips.map((tip, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default EducationPathways;
