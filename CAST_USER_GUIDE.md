# CAST Framework User Guide
## How to Use the Context-Aware Skills Translation Framework

The CAST (Context-Aware Skills Translation Framework) provides multilingual career guidance with cultural sensitivity for Indian languages. Here's how users can access and use it:

## 🚀 User Access Methods

### 1. **Web Interface (Primary Method)**

Users can access CAST through the CareerBuddy web application:

**URL:** `http://localhost:3000/cast-demo` (or your deployed URL)

**Navigation:** 
- Log into CareerBuddy
- Click the "🌐 CAST AI" button in the navigation bar
- Access the full CAST demo interface

### 2. **Integrated Career Recommendations**

CAST is automatically integrated into the main career recommendation flow:
- During assessments, translations are provided in the user's preferred language
- Cultural context is preserved in career descriptions
- Bias-free recommendations are generated

### 3. **API Access (For Developers)**

Direct API access for integration with other applications:

**Base URL:** `http://localhost:8000/api/cast`

## 📋 Available Features

### 🌍 1. Multilingual Translation

**Purpose:** Translate career content while preserving cultural context

**Supported Languages:**
- English (en)
- Hindi (hi) - हिंदी
- Tamil (ta) - தமிழ்
- Telugu (te) - తెలుగు
- Bengali (bn) - বাংলা
- Marathi (mr) - मराठी
- Gujarati (gu) - ગુજરાતી
- Kannada (kn) - ಕನ್ನಡ
- Malayalam (ml) - മലയാളം
- Punjabi (pa) - ਪੰਜਾਬੀ
- Odia (or) - ଓଡ଼ିଆ
- Assamese (as) - অসমীয়া
- Urdu (ur) - اردو
- Sindhi (sd) - سندھی
- Nepali (ne) - नेपाली
- Konkani (gom) - कोंकणी

**How to Use:**
1. Enter text in the "Translation" tab
2. Select source and target languages
3. Choose cultural region (North India, South India, etc.)
4. Click "Translate" to get culturally-aware translation

**Example Use Cases:**
- Translate "Software Developer" to Hindi with cultural context
- Convert technical skills to regional language equivalents
- Adapt job descriptions for local markets

### 🔍 2. Bias Detection & Analysis

**Purpose:** Identify and mitigate cultural, gender, and social biases in career content

**Features:**
- Detects multiple bias types (gender, cultural, socioeconomic)
- Provides severity ratings and explanations
- Suggests bias-free alternatives
- Risk level assessment

**How to Use:**
1. Go to "Bias Analysis" tab
2. Paste content to analyze
3. Select language and cultural context
4. Review detected biases and suggestions

**Example Scenarios:**
- Check job descriptions for gender bias
- Analyze career content for cultural insensitivity
- Validate educational materials for inclusivity

### 🗺️ 3. Cross-Cultural Skills Mapping

**Purpose:** Map skills across different cultural contexts and regions

**Features:**
- Traditional skill bridging (e.g., "Jugaad" → "Creative Problem Solving")
- Cultural equivalent identification
- Regional skill variations
- Confidence scoring for mappings

**How to Use:**
1. Access "Skills Mapping" tab
2. Enter skills separated by commas
3. Select source and target cultures
4. Review mapped skills with cultural insights

**Examples:**
- Map "Joint Family Management" to corporate leadership skills
- Translate "Rangoli Design" to "Creative Arts & Pattern Design"
- Convert regional crafts to modern skill categories

## 🎯 Step-by-Step Usage Guide

### For End Users (Career Seekers)

1. **Access the Platform**
   - Visit CareerBuddy website
   - Create account or log in
   - Navigate to CAST AI section

2. **Get Multilingual Career Guidance**
   - Take assessment in your preferred language
   - Receive culturally-relevant career recommendations
   - View job descriptions in local language context

3. **Use Translation Features**
   - Translate career terms to better understand opportunities
   - Get cultural context for international careers
   - Find local equivalents for global skills

4. **Check for Bias**
   - Analyze career advice for potential biases
   - Get inclusive alternatives to biased content
   - Ensure fair and equitable guidance

### For Counselors & Educators

1. **Content Creation**
   - Use bias detection to validate educational materials
   - Translate content for diverse student populations
   - Map traditional skills to modern career paths

2. **Personalized Guidance**
   - Provide culturally-sensitive career advice
   - Bridge language barriers with students
   - Offer inclusive career options

3. **Quality Assurance**
   - Validate translations for accuracy
   - Check content for cultural appropriateness
   - Ensure bias-free career recommendations

### For Developers & Integrators

1. **API Integration**
   ```bash
   # Check framework status
   curl http://localhost:8000/api/cast/health
   
   # Get supported languages
   curl http://localhost:8000/api/cast/languages
   
   # Translate content
   curl -X POST http://localhost:8000/api/cast/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "Software Developer", "source_language": "en", "target_language": "hi"}'
   ```

2. **Service Integration**
   ```typescript
   import { castAPI } from './services/castAPI';
   
   // Translate content
   const result = await castAPI.translateText({
     text: "Data Scientist",
     source_language: "en",
     target_language: "ta",
     cultural_region: "South India",
     content_type: "career"
   });
   ```

## 🔧 Configuration Options

### Translation Settings
- **Quality Threshold:** Minimum confidence score for translations
- **Cultural Preservation:** Level of cultural context to maintain
- **Alternative Suggestions:** Number of alternative translations

### Bias Detection Settings
- **Sensitivity Level:** How strict the bias detection should be
- **Auto-Mitigation:** Automatically apply bias-free alternatives
- **Warning Thresholds:** When to flag potential issues

### Skills Mapping Settings
- **Traditional Bridge:** Include traditional skill mappings
- **Cultural Weighting:** How much to weight cultural context
- **Confidence Threshold:** Minimum confidence for skill mappings

## 🚨 Best Practices

### For Users
1. **Provide Context:** Always specify cultural region and demographics
2. **Review Suggestions:** Check alternative translations and bias warnings
3. **Validate Results:** Use the validation feature for important translations
4. **Report Issues:** Provide feedback for continuous improvement

### For Developers
1. **Handle Errors:** Implement proper error handling for API calls
2. **Cache Results:** Use appropriate caching for frequently translated content
3. **Monitor Performance:** Track translation quality and response times
4. **Update Regularly:** Keep language models and cultural data current

### For Organizations
1. **Training:** Ensure staff understand cultural sensitivity principles
2. **Quality Control:** Regularly audit translated content
3. **Feedback Loop:** Collect user feedback for framework improvement
4. **Compliance:** Ensure adherence to diversity and inclusion policies

## 📊 Monitoring & Analytics

The framework provides comprehensive analytics:

- **Translation Usage:** Track which languages are most requested
- **Bias Detection Rates:** Monitor types and frequency of detected biases
- **Quality Metrics:** Track translation confidence and user satisfaction
- **Cultural Insights:** Understand regional preferences and patterns

## 🆘 Troubleshooting

### Common Issues

1. **Translation Not Available**
   - Check if target language is supported
   - Verify internet connection
   - Ensure proper API authentication

2. **Low Quality Translations**
   - Provide more context in the request
   - Check cultural region settings
   - Try alternative translation suggestions

3. **Bias Detection False Positives**
   - Adjust sensitivity levels
   - Provide more cultural context
   - Review suggested alternatives

4. **Skills Mapping Uncertainty**
   - Use more specific skill descriptions
   - Provide domain context
   - Check confidence scores

### Support Resources

- **Documentation:** Comprehensive API documentation
- **Examples:** Sample code and use cases
- **Community:** User forums and discussion groups
- **Support:** Direct technical support channels

## 🔮 Future Enhancements

Planned features for upcoming releases:

- **Voice Integration:** Audio translation capabilities
- **Real-time Translation:** Live translation during video calls
- **Expanded Languages:** Support for more Indian languages and dialects
- **Advanced AI:** Improved cultural context understanding
- **Mobile Apps:** Native mobile applications
- **Offline Mode:** Offline translation capabilities

---

*The CAST Framework is continuously evolving to better serve India's diverse linguistic and cultural landscape. Your feedback and usage patterns help us improve the system for everyone.*
