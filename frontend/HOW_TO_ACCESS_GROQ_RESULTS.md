# How to Access Groq Results from Frontend

## 🎯 Complete Guide to Accessing Groq Results

### 1. Overview: Data Flow
```
MARE Assessment → Backend API → Enhanced Results → Frontend Display
```

## 📊 Data Structure

### Enhanced Results Response Format:
```typescript
interface EnhancedMAREResponse {
  standard_recommendations: MARERecommendation[];
  groq_enhanced_suggestions: GroqEnhancedSuggestion[];
  career_pathway_summary: string | null;
  enhancement_available: boolean;
}

interface GroqEnhancedSuggestion {
  career_title: string;
  personalized_insight: string;
  actionable_steps: string[];
  skill_development_plan: string[];
  cultural_considerations: string;
  timeline_suggestion: string;
  confidence_score: number;
}
```

## 🔌 Frontend API Calls

### Method 1: Direct API Call (Recommended)
```typescript
// In your component
const fetchGroqResults = async (assessmentData: any) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch('/api/v1/mare/recommendations/enhanced', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(assessmentData)
    });

    if (response.ok) {
      const enhancedResults = await response.json();
      console.log('Groq enhanced results:', enhancedResults);
      
      // Access Groq suggestions
      const groqSuggestions = enhancedResults.groq_enhanced_suggestions;
      console.log('Groq suggestions:', groqSuggestions);
      
      return enhancedResults;
    }
  } catch (error) {
    console.error('Error fetching Groq results:', error);
  }
};
```

### Method 2: Using React State (Current Implementation)
```typescript
// Example component accessing Groq results
import React, { useState, useEffect } from 'react';

const MyGroqComponent: React.FC = () => {
  const [enhancedResults, setEnhancedResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAssessmentSubmit = async (formData: any) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setEnhancedResults(data);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Accessing Groq data
  const groqSuggestions = enhancedResults?.groq_enhanced_suggestions || [];
  const standardRecs = enhancedResults?.standard_recommendations || [];
  const careerPathway = enhancedResults?.career_pathway_summary || null;

  return (
    <div>
      {loading && <div>Loading Groq insights...</div>}
      
      {enhancedResults && (
        <>
          <h2>Standard Recommendations</h2>
          {standardRecs.map((rec, index) => (
            <div key={index}>
              <h3>{rec.title}</h3>
              <p>Score: {rec.overall_score}</p>
            </div>
          ))}

          <h2>Groq Enhanced Insights</h2>
          {groqSuggestions.map((suggestion, index) => (
            <div key={index} className="groq-suggestion">
              <h3>{suggestion.career_title}</h3>
              <p><strong>Insight:</strong> {suggestion.personalized_insight}</p>
              <p><strong>Cultural:</strong> {suggestion.cultural_considerations}</p>
              <p><strong>Timeline:</strong> {suggestion.timeline_suggestion}</p>
              
              <h4>Action Steps:</h4>
              <ul>
                {suggestion.actionable_steps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
              
              <h4>Skill Development:</h4>
              <ul>
                {suggestion.skill_development_plan.map((skill, i) => (
                  <li key={i}>{skill}</li>
                ))}
              </ul>
            </div>
          ))}
        </>
      )}
    </div>
  );
};
```

## 🎨 Accessing Groq Results in Different Components

### 1. From MAREAssessmentForm (Assessment Submission)
```typescript
// In MAREAssessmentForm.tsx
const handleSubmit = async () => {
  try {
    // Get enhanced recommendations (includes Groq)
    const enhancedResponse = await fetch('/api/v1/mare/recommendations/enhanced', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (enhancedResponse.ok) {
      const enhancedData = await enhancedResponse.json();
      
      // Navigate to results with Groq data
      navigate('/results', { 
        state: { 
          enhancedRecommendations: enhancedData,
          formData,
          source: 'MARE_ENHANCED'
        } 
      });
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### 2. From Results Page (Display Results)
```typescript
// In Results.tsx
const Results: React.FC = () => {
  const location = useLocation();
  const [enhancedResults, setEnhancedResults] = useState<any>(null);

  useEffect(() => {
    const navigationState = location.state as any;
    
    if (navigationState?.enhancedRecommendations) {
      const groqData = navigationState.enhancedRecommendations;
      setEnhancedResults(groqData);
      
      // Access Groq suggestions
      console.log('Groq suggestions:', groqData.groq_enhanced_suggestions);
    }
  }, [location.state]);

  return (
    <div>
      {enhancedResults && (
        <GroqEnhancedMAREResults 
          assessmentData={enhancedResults}
        />
      )}
    </div>
  );
};
```

### 3. Custom Hook for Groq Access
```typescript
// Custom hook: useGroqResults.ts
import { useState, useCallback } from 'react';

interface GroqResults {
  data: any;
  loading: boolean;
  error: string | null;
}

export const useGroqResults = () => {
  const [results, setResults] = useState<GroqResults>({
    data: null,
    loading: false,
    error: null
  });

  const fetchGroqResults = useCallback(async (assessmentData: any) => {
    setResults(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(assessmentData)
      });

      if (response.ok) {
        const data = await response.json();
        setResults({ data, loading: false, error: null });
        return data;
      } else {
        throw new Error('Failed to fetch Groq results');
      }
    } catch (error) {
      setResults(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
      return null;
    }
  }, []);

  return {
    ...results,
    fetchGroqResults,
    groqSuggestions: results.data?.groq_enhanced_suggestions || [],
    standardRecommendations: results.data?.standard_recommendations || [],
    careerPathway: results.data?.career_pathway_summary || null
  };
};

// Usage in component:
const MyComponent = () => {
  const { 
    groqSuggestions, 
    loading, 
    error, 
    fetchGroqResults 
  } = useGroqResults();

  const handleSubmit = async (formData: any) => {
    const results = await fetchGroqResults(formData);
    console.log('Groq results:', results);
  };

  return (
    <div>
      {loading && <div>Loading Groq insights...</div>}
      {error && <div>Error: {error}</div>}
      
      {groqSuggestions.map((suggestion, index) => (
        <div key={index}>
          <h3>{suggestion.career_title}</h3>
          <p>{suggestion.personalized_insight}</p>
        </div>
      ))}
    </div>
  );
};
```

## 🔍 Debugging Groq Results

### Check if Groq is Working:
```typescript
const debugGroqResults = (enhancedResults: any) => {
  console.log('=== GROQ DEBUG ===');
  console.log('Full response:', enhancedResults);
  console.log('Enhancement available:', enhancedResults?.enhancement_available);
  console.log('Groq suggestions count:', enhancedResults?.groq_enhanced_suggestions?.length || 0);
  
  if (enhancedResults?.groq_enhanced_suggestions?.length > 0) {
    console.log('✅ Groq is working!');
    console.log('First Groq suggestion:', enhancedResults.groq_enhanced_suggestions[0]);
  } else {
    console.log('❌ No Groq suggestions found');
    console.log('Check backend logs for Groq API key configuration');
  }
};
```

### Browser Console Commands:
```javascript
// Check if assessment data exists
console.log('Assessment data:', localStorage.getItem('mareAssessmentData'));

// Check authentication
console.log('Auth token:', localStorage.getItem('token'));

// Manual API test
fetch('/api/v1/mare/recommendations/enhanced', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  },
  body: JSON.stringify({
    age: 25,
    education_level: "Bachelor's",
    location: "Mumbai",
    skills: ["Python", "JavaScript"],
    interests: ["Technology", "Innovation"]
  })
})
.then(r => r.json())
.then(data => console.log('Groq results:', data));
```

## 📱 Real Example from Current Implementation

Looking at your current `GroqEnhancedMAREResults.tsx`:

```typescript
// How results are accessed in your component:
const GroqEnhancedMAREResults: React.FC<Props> = ({ assessmentData, onBack }) => {
  const [results, setResults] = useState<EnhancedMAREResponse | null>(null);

  const fetchEnhancedRecommendations = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch('/api/v1/mare/recommendations/enhanced', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(assessmentData)
    });

    if (response.ok) {
      const data = await response.json();
      setResults(data); // This contains Groq results!
      
      // Access Groq suggestions:
      const groqSuggestions = data.groq_enhanced_suggestions;
      console.log('Groq suggestions:', groqSuggestions);
    }
  };

  // In your JSX, you can access:
  return (
    <div>
      {results?.groq_enhanced_suggestions.map((suggestion, index) => (
        <div key={index}>
          <h3>{suggestion.career_title}</h3>
          <p>{suggestion.personalized_insight}</p>
          <p>{suggestion.cultural_considerations}</p>
          <ul>
            {suggestion.actionable_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};
```

## 🎯 Quick Test

To test Groq results right now:

1. **Complete MARE assessment** at `/mare-assessment`
2. **Check browser console** for API responses
3. **Look for enhanced results** with `groq_enhanced_suggestions` array
4. **If empty**, check backend logs for Groq API key issues

The key is that Groq results come as part of the enhanced API response - you don't need a separate API call!
