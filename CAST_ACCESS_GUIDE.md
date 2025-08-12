# How Users Access the CAST Framework

## 🎯 Overview

The Context-Aware Skills Translation Framework (CAST-F) is accessible through multiple interfaces designed for different user types and use cases. Here's how users can access and benefit from CAST:

## 🌐 Web Interface (Primary Access Method)

### Direct Demo Access
- **URL:** `http://localhost:3001/cast-demo` (development) or your deployed URL
- **Navigation:** Login → Click "🌐 CAST AI" button in navigation bar
- **Features Available:**
  - Interactive translation interface
  - Real-time bias analysis
  - Cross-cultural skills mapping
  - Language selection (16+ Indian languages)
  - Cultural region customization

### Integrated Experience
- **Assessments:** CAST automatically provides translations during career assessments
- **Results:** Career recommendations include culturally-adapted content
- **Progress Tracking:** Multilingual progress reports and analytics

## 📱 User Journey

### 1. **New Users**
```
Visit CareerBuddy → Sign Up → Navigate to CAST Demo → Explore Features
```

### 2. **Existing Users**
```
Login → Dashboard → Click "🌐 CAST AI" → Access Full CAST Interface
```

### 3. **During Assessment**
```
Take Assessment → Language Auto-Detection → Culturally-Adapted Questions → Bias-Free Recommendations
```

## 🔧 Developer & Integration Access

### REST API Endpoints
```bash
# Base URL: http://localhost:8000/api/cast

# Check framework status
GET /health

# Get supported languages
GET /languages

# Translate content
POST /translate
{
  "text": "Software Developer",
  "source_language": "en", 
  "target_language": "hi",
  "cultural_region": "North India"
}

# Analyze bias
POST /analyze-bias
{
  "content": "Job description text",
  "language": "en"
}

# Map skills across cultures  
POST /map-skills
{
  "skills": ["teamwork", "leadership"],
  "source_culture": "Western",
  "target_culture": "Indian"
}
```

### JavaScript/TypeScript Integration
```typescript
import { castAPI } from './services/castAPI';

// Translate career content
const translation = await castAPI.translateText({
  text: "Data Scientist",
  source_language: "en",
  target_language: "ta",
  cultural_region: "South India",
  content_type: "career"
});

// Check for bias
const biasAnalysis = await castAPI.analyzeBias({
  content: "Career description text",
  language: "en"
});
```

## 👥 User Types & Access Patterns

### 🎓 **Students & Job Seekers**
- **Primary Access:** Web interface at `/cast-demo`
- **Use Cases:**
  - Translate career descriptions to native language
  - Understand skill requirements in cultural context
  - Get bias-free career recommendations
  - Map traditional skills to modern careers

### 👨‍🏫 **Career Counselors & Educators**
- **Primary Access:** Web interface + API integration
- **Use Cases:**
  - Create multilingual career guidance materials
  - Validate content for cultural sensitivity
  - Bridge language barriers with students
  - Ensure inclusive career recommendations

### 👩‍💻 **Developers & Organizations**
- **Primary Access:** REST API + TypeScript SDK
- **Use Cases:**
  - Integrate CAST into existing platforms
  - Build multilingual career applications
  - Automate bias detection in content
  - Create culturally-aware recruitment tools

### 🏢 **HR & Recruitment Teams**
- **Primary Access:** Web interface + API
- **Use Cases:**
  - Create inclusive job descriptions
  - Translate opportunities for diverse candidates
  - Remove bias from recruitment content
  - Understand cultural skill equivalents

## 🚀 Getting Started

### For End Users
1. **Visit:** `http://localhost:3001/cast-demo`
2. **Select:** Your preferred language and cultural region
3. **Choose:** Translation, Bias Analysis, or Skills Mapping
4. **Input:** Your content and get instant results
5. **Review:** Cultural adaptations and alternative suggestions

### For Developers
1. **Check API:** `curl http://localhost:8000/api/cast/health`
2. **Get Languages:** `curl http://localhost:8000/api/cast/languages`
3. **Test Translation:** Use POST request to `/translate` endpoint
4. **Integrate:** Use TypeScript SDK for seamless integration
5. **Monitor:** Track usage and quality metrics

## 📊 Features Available to Users

### 🌍 **Multilingual Translation**
- 16+ Indian languages supported
- Cultural context preservation
- Alternative translation suggestions
- Confidence scoring
- Domain-specific translations (career, education, skills)

### 🔍 **Bias Detection & Mitigation**
- Gender bias detection
- Cultural bias identification
- Socioeconomic bias analysis
- Severity ratings and explanations
- Bias-free alternative suggestions

### 🗺️ **Cross-Cultural Skills Mapping**
- Traditional skill bridging
- Regional skill variations
- Cultural equivalent identification
- Confidence scoring for mappings
- Industry-specific mappings

### 📈 **Quality Assurance**
- Translation validation
- Cultural appropriateness checks
- User feedback integration
- Continuous learning and improvement

## 🔒 Security & Privacy

- **Data Protection:** All user data is encrypted and protected
- **Privacy:** No personal information stored without consent
- **Anonymization:** Content analysis doesn't retain personal details
- **Compliance:** Adheres to data protection regulations

## 📞 Support & Resources

### Documentation
- **User Guide:** Comprehensive usage documentation
- **API Documentation:** Technical integration guides
- **Examples:** Sample code and use cases
- **Best Practices:** Guidelines for optimal usage

### Community & Support
- **Forum:** User community for questions and discussions
- **Support:** Direct technical support channels
- **Feedback:** Continuous improvement through user input
- **Training:** Workshops and educational resources

## 📈 Usage Analytics (Available to Admins)

- **Translation Volume:** Track usage patterns by language
- **Quality Metrics:** Monitor translation confidence and accuracy
- **Bias Detection Rates:** Analyze types and frequency of detected biases
- **User Satisfaction:** Feedback and rating analytics
- **Cultural Insights:** Understand regional preferences and patterns

---

## 🌟 Quick Start Commands

```bash
# Start backend server
cd backend && uvicorn app.main:app --reload

# Start frontend 
cd frontend && npm run dev

# Access CAST Demo
# Navigate to: http://localhost:3001/cast-demo

# Test API directly
curl http://localhost:8000/api/cast/health
```

**The CAST Framework is designed to be accessible, inclusive, and culturally sensitive - making career guidance available to everyone regardless of language or cultural background.**
