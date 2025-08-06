# SVM Career Predictor Integration Guide

## 🎯 Overview

The SVM (Support Vector Machine) Career Predictor is a new machine learning component integrated into CareerBuddy that predicts:

- **Next Job Position** - Most likely job title/role
- **Institution Type** - Recommended workplace type (startup, corporate, etc.)
- **Career Transition** - Career progression timeline
- **Salary Range** - Expected compensation range

## 🚀 Quick Start

### 1. Install Dependencies
All required ML libraries are already included in `requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

### 2. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload
```

### 3. Access New API Endpoints
- **API Documentation**: http://localhost:8000/docs
- **SVM Endpoints**: `/recommend/v2/svm/*`

## 📊 Training the SVM Models

### Option 1: Using the API (Recommended)
```bash
# Train models using the API
curl -X POST "http://localhost:8000/recommend/v2/svm/train" \
     -H "Content-Type: application/json"
```

### Option 2: Using Training Data
Place your training CSV file in `backend/svm_training_data.csv` with columns:
```
Education Level,Current Course,Current Marks,Marks Type,10th Percentage,12th Percentage,Location,Residence Type,Family Background,Interests,Skills,Career Goals,Next Job,Next Institution,Career Transition,Salary Range
```

### Option 3: Using the Test Script
```bash
python test_svm_integration.py
```

## 🌐 New API Endpoints

### 1. Get SVM Predictions
```http
POST /recommend/v2/svm/predict
Content-Type: application/json

{
  "user_id": 123,
  "education_level": "Undergraduate",
  "current_course": "B.Tech Computer Science",
  "current_marks_value": 8.5,
  "current_marks_type": "CGPA",
  "tenth_percentage": 88.5,
  "twelfth_percentage": 91.2,
  "place_of_residence": "Mumbai",
  "residence_type": "Metro",
  "family_background": "Middle Income",
  "interests": "Coding|AI|Gaming",
  "skills": "Python|Web Development|Problem Solving",
  "career_goals": "Software Engineering",
  "language": "en"
}
```

**Response:**
```json
{
  "user_id": 123,
  "svm_predictions": {
    "predictions": {
      "next_job": "Software Developer",
      "next_institution": "Tech Company",
      "career_transition": "Entry Level",
      "salary_range": "6-10 LPA"
    },
    "confidences": {
      "next_job": 0.87,
      "next_institution": 0.82,
      "career_transition": 0.79,
      "salary_range": 0.84
    },
    "insights": {
      "summary": ["Most likely next job: Software Developer (confidence: 0.87)"],
      "recommendations": ["High confidence predictions - career path is well-aligned"],
      "next_steps": ["Review the predicted career path", "Identify skill gaps"]
    }
  }
}
```

### 2. Train SVM Models
```http
POST /recommend/v2/svm/train?retrain=false
```

### 3. Get Model Information
```http
GET /recommend/v2/svm/model-info
```

### 4. Enhanced Hybrid Recommendations (NEW)
```http
POST /recommend/v2/hybrid-with-svm
```
This endpoint combines content-based (50%), collaborative (30%), and SVM (20%) recommendations.

## 🔧 Configuration

### Model Weights (in `hybrid_recommender.py`)
```python
self.content_weight = 0.5      # Content-based filtering
self.collaborative_weight = 0.3 # Collaborative filtering  
self.svm_weight = 0.2          # SVM predictions
```

### SVM Parameters (in `svm_predictor.py`)
```python
self.svm_params = {
    'kernel': 'rbf',
    'C': 1.0,
    'gamma': 'scale',
    'probability': True,
    'random_state': 42
}
```

## 📁 File Structure Changes

### New Files Added:
```
backend/app/logic/svm_predictor.py        # Main SVM predictor class
backend/models/                           # Model storage directory
backend/svm_training_data.csv            # Sample training data
test_svm_integration.py                   # Test script
SVM_INTEGRATION_GUIDE.md                 # This guide
```

### Modified Files:
```
backend/app/logic/hybrid_recommender.py  # Updated with SVM integration
backend/app/api/recommend.py             # New SVM endpoints
backend/app/db/crud.py                   # Added career outcomes functions
backend/app/logic/data_processor.py      # Added load_career_data method
README.md                                # Updated documentation
```

## 🧪 Testing

### Run Integration Tests
```bash
python test_svm_integration.py
```

### Test Individual Components
```python
# Test SVM predictor
from backend.app.logic.svm_predictor import SVMCareerPredictor
predictor = SVMCareerPredictor()
model_info = predictor.get_model_info()

# Test hybrid integration  
from backend.app.logic.hybrid_recommender import HybridRecommendationEngine
engine = HybridRecommendationEngine()
print(f"SVM Weight: {engine.svm_weight}")
```

## 🎯 Usage Examples

### Frontend Integration
```typescript
// Get SVM predictions
const svmPredictions = await api.post('/recommend/v2/svm/predict', userProfile);

// Get enhanced hybrid recommendations
const hybridRecs = await api.post('/recommend/v2/hybrid-with-svm', userProfile);

// Display SVM insights
const { predictions, confidences, insights } = svmPredictions.svm_predictions;
console.log(`Predicted next job: ${predictions.next_job} (${confidences.next_job})`);
```

### Training New Models
```python
# Retrain with new data
training_result = await fetch('/recommend/v2/svm/train?retrain=true', {
    method: 'POST'
});
```

## 🚨 Troubleshooting

### Common Issues:

1. **Models not trained**: Run the training endpoint first
2. **Import errors**: Ensure all dependencies are installed
3. **Low prediction confidence**: Add more training data
4. **Feature engineering errors**: Check input data format

### Debug Mode:
Set `DEBUG=true` in environment variables for detailed logging.

### Fallback Behavior:
- If SVM models aren't trained, the system provides default predictions
- If SVM fails, the hybrid recommender continues with content + collaborative only
- All SVM errors are logged and don't break the main recommendation flow

## 📈 Performance Monitoring

### Model Metrics:
- **Training Accuracy**: Available in model metadata
- **Prediction Confidence**: Returned with each prediction
- **Feature Importance**: Available through model analysis

### API Performance:
- **Response Time**: Monitor via `/docs` endpoint
- **Cache Usage**: SVM predictions are cached for performance
- **Error Rates**: Check application logs

## 🔄 Model Updates

### Scheduled Retraining:
```bash
# Add to cron job for periodic retraining
0 2 * * 0 curl -X POST "http://localhost:8000/recommend/v2/svm/train?retrain=true"
```

### Manual Updates:
1. Add new training data to CSV
2. Call the training endpoint
3. Monitor accuracy metrics
4. Deploy updated models

## 📋 Next Steps

1. **Monitor Performance**: Track prediction accuracy and user feedback
2. **Expand Training Data**: Collect more diverse career outcome data
3. **Feature Enhancement**: Add more sophisticated features
4. **Model Ensemble**: Consider combining multiple ML algorithms
5. **Real-time Learning**: Implement online learning capabilities

---

🎉 **SVM Integration Complete!** 

Your CareerBuddy platform now includes state-of-the-art machine learning predictions for enhanced career guidance.
