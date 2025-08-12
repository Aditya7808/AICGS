-- Insert 100 Diverse Career Opportunities for MARE AI System
-- This file populates the career_opportunities table with realistic data for Indian context

-- Clear existing data (optional - remove this line if you want to keep existing data)
-- TRUNCATE TABLE career_opportunities RESTART IDENTITY CASCADE;

-- Technology Careers (20 opportunities)
INSERT INTO career_opportunities (
    title, industry, description, required_skills, preferred_skills, experience_level,
    salary_range_min, salary_range_max, currency, location, remote_available,
    urban_rural_suitability, traditional_modern_spectrum, cultural_adaptability_score,
    economic_accessibility_score, geographic_flexibility_score, family_acceptance_score,
    growth_potential_score, job_security_score, automation_risk_score, future_outlook,
    mare_compatibility_score, is_active
) VALUES

-- Technology Careers
('Software Developer', 'Technology', 'Design, develop, and maintain software applications and systems', 
 ARRAY['Programming', 'Problem Solving', 'Software Development', 'Computer Science'], 
 ARRAY['Java', 'Python', 'React', 'Database Management'], 'entry', 
 400000, 800000, 'INR', 'Bangalore', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.8, 0.9, 0.7, 0.3, 'booming', 0.85, true),

('Data Scientist', 'Technology', 'Analyze complex data to help organizations make informed decisions',
 ARRAY['Statistics', 'Python', 'Machine Learning', 'Data Analysis'],
 ARRAY['R', 'SQL', 'Deep Learning', 'Big Data'], 'mid', 
 600000, 1200000, 'INR', 'Hyderabad', true, 'urban', 'modern', 0.7, 0.6, 0.8, 0.7, 0.9, 0.8, 0.2, 'booming', 0.88, true),

('Cybersecurity Analyst', 'Technology', 'Protect organizations from cyber threats and security breaches',
 ARRAY['Network Security', 'Risk Assessment', 'Security Tools', 'Problem Solving'],
 ARRAY['Ethical Hacking', 'Cryptography', 'Incident Response'], 'mid',
 500000, 1000000, 'INR', 'Pune', false, 'urban', 'modern', 0.8, 0.7, 0.6, 0.8, 0.9, 0.9, 0.1, 'booming', 0.82, true),

('Mobile App Developer', 'Technology', 'Create mobile applications for iOS and Android platforms',
 ARRAY['Mobile Development', 'Programming', 'UI/UX Design', 'Problem Solving'],
 ARRAY['React Native', 'Flutter', 'Swift', 'Kotlin'], 'entry',
 350000, 700000, 'INR', 'Mumbai', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.7, 0.8, 0.7, 0.3, 'growing', 0.80, true),

('DevOps Engineer', 'Technology', 'Bridge development and operations teams to improve software deployment',
 ARRAY['System Administration', 'Cloud Computing', 'Automation', 'Linux'],
 ARRAY['Docker', 'Kubernetes', 'AWS', 'CI/CD'], 'mid',
 550000, 1100000, 'INR', 'Chennai', true, 'urban', 'modern', 0.7, 0.6, 0.8, 0.7, 0.9, 0.8, 0.2, 'booming', 0.83, true),

-- Healthcare Careers
('Software Tester', 'Technology', 'Ensure software quality through systematic testing and validation',
 ARRAY['Testing', 'Attention to Detail', 'Problem Solving', 'Documentation'],
 ARRAY['Automation Testing', 'Selenium', 'API Testing'], 'entry',
 300000, 600000, 'INR', 'Gurgaon', true, 'urban', 'balanced', 0.9, 0.8, 0.8, 0.9, 0.7, 0.8, 0.2, 'growing', 0.78, true),

('UI/UX Designer', 'Technology', 'Design user interfaces and experiences for digital products',
 ARRAY['Design', 'User Research', 'Prototyping', 'Creativity'],
 ARRAY['Figma', 'Adobe Creative Suite', 'User Testing'], 'entry',
 350000, 750000, 'INR', 'Delhi', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.8, 0.8, 0.7, 0.3, 'growing', 0.79, true),

('Database Administrator', 'Technology', 'Manage and maintain database systems for organizations',
 ARRAY['Database Management', 'SQL', 'System Administration', 'Problem Solving'],
 ARRAY['Oracle', 'MongoDB', 'Performance Tuning'], 'mid',
 450000, 900000, 'INR', 'Noida', false, 'urban', 'balanced', 0.8, 0.7, 0.7, 0.8, 0.7, 0.9, 0.2, 'stable', 0.76, true),

('Network Engineer', 'Technology', 'Design, implement, and maintain computer networks',
 ARRAY['Networking', 'TCP/IP', 'Router Configuration', 'Problem Solving'],
 ARRAY['Cisco', 'Network Security', 'Cloud Networking'], 'mid',
 400000, 800000, 'INR', 'Bangalore', false, 'urban', 'balanced', 0.8, 0.7, 0.6, 0.8, 0.7, 0.8, 0.3, 'stable', 0.75, true),

('Product Manager', 'Technology', 'Define product strategy and coordinate development teams',
 ARRAY['Product Management', 'Strategy', 'Communication', 'Leadership'],
 ARRAY['Agile', 'Market Research', 'Analytics'], 'senior',
 800000, 1600000, 'INR', 'Mumbai', true, 'urban', 'modern', 0.8, 0.5, 0.8, 0.7, 0.9, 0.8, 0.1, 'booming', 0.84, true),

-- Healthcare Careers (15 opportunities)
('Doctor (General Medicine)', 'Healthcare', 'Diagnose and treat various medical conditions',
 ARRAY['Medical Knowledge', 'Patient Care', 'Communication', 'Problem Solving'],
 ARRAY['Emergency Medicine', 'Surgery', 'Research'], 'senior',
 800000, 2000000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.6, 0.5, 0.9, 0.8, 0.9, 0.1, 'growing', 0.87, true),

('Registered Nurse', 'Healthcare', 'Provide patient care and support in medical settings',
 ARRAY['Patient Care', 'Medical Knowledge', 'Communication', 'Empathy'],
 ARRAY['ICU Care', 'Pediatrics', 'Emergency Care'], 'entry',
 300000, 600000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.6, 0.9, 0.7, 0.8, 0.1, 'growing', 0.85, true),

('Pharmacist', 'Healthcare', 'Dispense medications and provide pharmaceutical care',
 ARRAY['Pharmaceutical Knowledge', 'Patient Counseling', 'Attention to Detail'],
 ARRAY['Clinical Pharmacy', 'Drug Information'], 'entry',
 250000, 500000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.8, 0.7, 0.8, 0.2, 'stable', 0.80, true),

('Physiotherapist', 'Healthcare', 'Help patients recover from injuries and improve mobility',
 ARRAY['Physical Therapy', 'Patient Care', 'Exercise Science', 'Communication'],
 ARRAY['Sports Therapy', 'Neurological Rehabilitation'], 'entry',
 300000, 700000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.7, 0.6, 0.8, 0.8, 0.7, 0.1, 'growing', 0.82, true),

('Medical Laboratory Technician', 'Healthcare', 'Conduct laboratory tests and analyze medical samples',
 ARRAY['Laboratory Skills', 'Attention to Detail', 'Medical Knowledge'],
 ARRAY['Pathology', 'Microbiology', 'Quality Control'], 'entry',
 200000, 400000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.8, 0.7, 0.8, 0.7, 0.8, 0.2, 'stable', 0.78, true),

('Radiologic Technologist', 'Healthcare', 'Operate imaging equipment for medical diagnosis',
 ARRAY['Medical Imaging', 'Technical Skills', 'Patient Care'],
 ARRAY['CT Scan', 'MRI', 'Ultrasound'], 'entry',
 300000, 600000, 'INR', 'Urban Areas', false, 'urban', 'traditional', 0.8, 0.7, 0.6, 0.8, 0.7, 0.8, 0.3, 'stable', 0.79, true),

('Dentist', 'Healthcare', 'Diagnose and treat dental and oral health issues',
 ARRAY['Dental Knowledge', 'Manual Dexterity', 'Patient Care'],
 ARRAY['Oral Surgery', 'Orthodontics', 'Cosmetic Dentistry'], 'senior',
 600000, 1500000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.6, 0.5, 0.9, 0.8, 0.8, 0.1, 'stable', 0.84, true),

('Health Information Technician', 'Healthcare', 'Manage patient health information and medical records',
 ARRAY['Medical Coding', 'Data Management', 'Attention to Detail'],
 ARRAY['Healthcare IT', 'HIPAA Compliance'], 'entry',
 250000, 500000, 'INR', 'Urban Areas', true, 'urban', 'balanced', 0.7, 0.8, 0.8, 0.7, 0.7, 0.7, 0.4, 'growing', 0.75, true),

('Nutritionist', 'Healthcare', 'Provide dietary advice and nutrition counseling',
 ARRAY['Nutrition Science', 'Counseling', 'Communication'],
 ARRAY['Sports Nutrition', 'Clinical Nutrition'], 'entry',
 200000, 500000, 'INR', 'All India', true, 'both', 'balanced', 0.8, 0.7, 0.8, 0.8, 0.8, 0.7, 0.2, 'growing', 0.81, true),

('Biomedical Engineer', 'Healthcare', 'Develop medical devices and healthcare technology',
 ARRAY['Engineering', 'Medical Knowledge', 'Problem Solving'],
 ARRAY['Medical Devices', 'Biomaterials', 'Research'], 'mid',
 500000, 1000000, 'INR', 'Bangalore', false, 'urban', 'modern', 0.7, 0.6, 0.7, 0.7, 0.9, 0.8, 0.2, 'booming', 0.83, true),

-- Finance & Business (15 opportunities)
('Financial Analyst', 'Finance', 'Analyze financial data and provide investment recommendations',
 ARRAY['Financial Analysis', 'Excel', 'Accounting', 'Mathematics'],
 ARRAY['Financial Modeling', 'Valuation', 'Risk Analysis'], 'entry',
 400000, 800000, 'INR', 'Mumbai', false, 'urban', 'traditional', 0.8, 0.6, 0.7, 0.8, 0.8, 0.7, 0.3, 'growing', 0.79, true),

('Chartered Accountant', 'Finance', 'Provide accounting, auditing, and financial advisory services',
 ARRAY['Accounting', 'Taxation', 'Auditing', 'Financial Reporting'],
 ARRAY['International Accounting', 'Forensic Accounting'], 'senior',
 600000, 1500000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.7, 0.6, 0.9, 0.8, 0.8, 0.2, 'stable', 0.86, true),

('Investment Banker', 'Finance', 'Facilitate financial transactions and investment deals',
 ARRAY['Financial Modeling', 'Valuation', 'Communication', 'Mathematics'],
 ARRAY['M&A', 'Capital Markets', 'Risk Management'], 'senior',
 1000000, 2500000, 'INR', 'Mumbai', false, 'urban', 'modern', 0.7, 0.4, 0.6, 0.7, 0.9, 0.6, 0.3, 'growing', 0.78, true),

('Banking Relationship Manager', 'Finance', 'Manage client relationships and provide banking solutions',
 ARRAY['Relationship Management', 'Sales', 'Banking Knowledge', 'Communication'],
 ARRAY['Wealth Management', 'Credit Analysis'], 'mid',
 400000, 900000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.7, 0.6, 0.8, 0.7, 0.8, 0.3, 'stable', 0.81, true),

('Insurance Agent', 'Finance', 'Sell insurance policies and provide customer service',
 ARRAY['Sales', 'Communication', 'Customer Service', 'Insurance Knowledge'],
 ARRAY['Risk Assessment', 'Claims Processing'], 'entry',
 200000, 600000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.8, 0.7, 0.7, 0.4, 'stable', 0.77, true),

('Tax Consultant', 'Finance', 'Provide tax planning and compliance services',
 ARRAY['Taxation', 'Accounting', 'Legal Knowledge', 'Attention to Detail'],
 ARRAY['International Tax', 'GST', 'Income Tax'], 'mid',
 300000, 800000, 'INR', 'All India', true, 'both', 'traditional', 0.8, 0.7, 0.8, 0.8, 0.7, 0.8, 0.3, 'stable', 0.80, true),

('Business Analyst', 'Business', 'Analyze business processes and recommend improvements',
 ARRAY['Business Analysis', 'Problem Solving', 'Communication', 'Data Analysis'],
 ARRAY['Process Improvement', 'Requirements Gathering'], 'mid',
 500000, 1000000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.8, 0.7, 0.8, 0.7, 0.3, 'growing', 0.81, true),

('Human Resources Manager', 'Business', 'Manage employee relations and organizational development',
 ARRAY['HR Management', 'Communication', 'Leadership', 'Conflict Resolution'],
 ARRAY['Talent Acquisition', 'Performance Management'], 'senior',
 600000, 1200000, 'INR', 'All India', false, 'both', 'balanced', 0.9, 0.7, 0.7, 0.8, 0.7, 0.8, 0.2, 'stable', 0.82, true),

('Marketing Manager', 'Business', 'Develop and execute marketing strategies and campaigns',
 ARRAY['Marketing', 'Communication', 'Creativity', 'Strategy'],
 ARRAY['Digital Marketing', 'Brand Management', 'Analytics'], 'mid',
 500000, 1200000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.8, 0.7, 0.8, 0.7, 0.3, 'growing', 0.83, true),

('Operations Manager', 'Business', 'Oversee daily operations and improve efficiency',
 ARRAY['Operations Management', 'Leadership', 'Problem Solving', 'Process Improvement'],
 ARRAY['Supply Chain', 'Quality Management'], 'senior',
 700000, 1400000, 'INR', 'All India', false, 'both', 'balanced', 0.8, 0.7, 0.7, 0.8, 0.8, 0.8, 0.2, 'stable', 0.83, true),

-- Education (10 opportunities)
('Primary School Teacher', 'Education', 'Teach young children fundamental academic skills',
 ARRAY['Teaching', 'Patience', 'Communication', 'Child Psychology'],
 ARRAY['Classroom Management', 'Curriculum Development'], 'entry',
 200000, 400000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.8, 0.9, 0.6, 0.9, 0.1, 'stable', 0.88, true),

('Secondary School Teacher', 'Education', 'Teach specific subjects to adolescent students',
 ARRAY['Subject Expertise', 'Teaching', 'Communication', 'Classroom Management'],
 ARRAY['Educational Technology', 'Special Education'], 'entry',
 250000, 500000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.8, 0.9, 0.6, 0.9, 0.1, 'stable', 0.87, true),

('College Professor', 'Education', 'Teach and conduct research at higher education level',
 ARRAY['Subject Expertise', 'Research', 'Teaching', 'Academic Writing'],
 ARRAY['Grant Writing', 'Publication', 'Mentoring'], 'senior',
 500000, 1200000, 'INR', 'All India', true, 'both', 'traditional', 0.8, 0.7, 0.7, 0.8, 0.8, 0.9, 0.1, 'stable', 0.85, true),

('Educational Counselor', 'Education', 'Guide students in academic and career planning',
 ARRAY['Counseling', 'Communication', 'Psychology', 'Career Guidance'],
 ARRAY['Student Assessment', 'Crisis Intervention'], 'mid',
 300000, 600000, 'INR', 'All India', true, 'both', 'balanced', 0.9, 0.8, 0.8, 0.8, 0.7, 0.8, 0.1, 'growing', 0.84, true),

('Training and Development Specialist', 'Education', 'Design and deliver employee training programs',
 ARRAY['Training Design', 'Facilitation', 'Communication', 'Adult Learning'],
 ARRAY['E-learning', 'Performance Analysis'], 'mid',
 400000, 800000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.8, 0.7, 0.8, 0.7, 0.2, 'growing', 0.81, true),

('Librarian', 'Education', 'Manage library resources and assist with research',
 ARRAY['Information Management', 'Research Skills', 'Communication', 'Organization'],
 ARRAY['Digital Libraries', 'Database Management'], 'entry',
 200000, 450000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.8, 0.6, 0.8, 0.3, 'stable', 0.79, true),

('Instructional Designer', 'Education', 'Design educational curricula and learning materials',
 ARRAY['Curriculum Design', 'Educational Technology', 'Communication', 'Creativity'],
 ARRAY['Learning Management Systems', 'Assessment Design'], 'mid',
 400000, 800000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.7, 0.7, 0.9, 0.7, 0.8, 0.7, 0.3, 'growing', 0.80, true),

('School Administrator', 'Education', 'Manage school operations and educational programs',
 ARRAY['Leadership', 'Administration', 'Education Policy', 'Communication'],
 ARRAY['Budget Management', 'Strategic Planning'], 'senior',
 500000, 1000000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.7, 0.6, 0.8, 0.7, 0.8, 0.1, 'stable', 0.82, true),

('Corporate Trainer', 'Education', 'Provide professional development training in corporate settings',
 ARRAY['Training', 'Communication', 'Subject Expertise', 'Facilitation'],
 ARRAY['Leadership Development', 'Sales Training'], 'mid',
 500000, 1000000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.6, 0.8, 0.7, 0.8, 0.7, 0.2, 'growing', 0.82, true),

('Educational Technology Specialist', 'Education', 'Integrate technology into educational settings',
 ARRAY['Educational Technology', 'Training', 'Technical Support', 'Problem Solving'],
 ARRAY['Learning Management Systems', 'Digital Tools'], 'mid',
 400000, 800000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.7, 0.7, 0.8, 0.7, 0.8, 0.7, 0.3, 'booming', 0.81, true),

-- Engineering (10 opportunities)
('Civil Engineer', 'Engineering', 'Design and supervise construction of infrastructure projects',
 ARRAY['Engineering Design', 'Construction Management', 'Mathematics', 'Problem Solving'],
 ARRAY['AutoCAD', 'Project Management', 'Environmental Engineering'], 'entry',
 300000, 700000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.7, 0.6, 0.8, 0.8, 0.8, 0.2, 'growing', 0.82, true),

('Mechanical Engineer', 'Engineering', 'Design, develop, and test mechanical systems',
 ARRAY['Mechanical Design', 'CAD', 'Manufacturing', 'Problem Solving'],
 ARRAY['3D Modeling', 'Automation', 'Quality Control'], 'entry',
 350000, 750000, 'INR', 'Multiple Cities', false, 'urban', 'traditional', 0.8, 0.7, 0.7, 0.8, 0.8, 0.7, 0.3, 'stable', 0.80, true),

('Electrical Engineer', 'Engineering', 'Design and maintain electrical systems and equipment',
 ARRAY['Electrical Systems', 'Circuit Design', 'Mathematics', 'Problem Solving'],
 ARRAY['Power Systems', 'Control Systems', 'Electronics'], 'entry',
 350000, 800000, 'INR', 'Multiple Cities', false, 'urban', 'traditional', 0.8, 0.7, 0.7, 0.8, 0.8, 0.8, 0.3, 'growing', 0.81, true),

('Chemical Engineer', 'Engineering', 'Design chemical processes and manufacturing systems',
 ARRAY['Chemical Processes', 'Mathematics', 'Process Design', 'Safety'],
 ARRAY['Process Optimization', 'Quality Control'], 'mid',
 400000, 900000, 'INR', 'Industrial Areas', false, 'urban', 'traditional', 0.7, 0.6, 0.6, 0.7, 0.8, 0.8, 0.2, 'stable', 0.78, true),

('Environmental Engineer', 'Engineering', 'Develop solutions for environmental problems',
 ARRAY['Environmental Science', 'Engineering', 'Problem Solving', 'Sustainability'],
 ARRAY['Water Treatment', 'Air Quality', 'Waste Management'], 'mid',
 400000, 800000, 'INR', 'Multiple Cities', false, 'both', 'modern', 0.8, 0.7, 0.7, 0.8, 0.9, 0.8, 0.1, 'booming', 0.85, true),

('Aerospace Engineer', 'Engineering', 'Design aircraft, spacecraft, and related systems',
 ARRAY['Aerospace Engineering', 'Mathematics', 'Physics', 'CAD'],
 ARRAY['Flight Testing', 'Propulsion Systems'], 'mid',
 600000, 1200000, 'INR', 'Bangalore', false, 'urban', 'modern', 0.6, 0.5, 0.5, 0.6, 0.9, 0.8, 0.2, 'growing', 0.75, true),

('Industrial Engineer', 'Engineering', 'Optimize complex systems and processes',
 ARRAY['Process Optimization', 'Systems Analysis', 'Mathematics', 'Problem Solving'],
 ARRAY['Lean Manufacturing', 'Six Sigma', 'Supply Chain'], 'mid',
 450000, 900000, 'INR', 'Multiple Cities', false, 'urban', 'balanced', 0.8, 0.7, 0.7, 0.7, 0.8, 0.8, 0.3, 'stable', 0.81, true),

('Automotive Engineer', 'Engineering', 'Design and develop automotive systems and vehicles',
 ARRAY['Automotive Engineering', 'CAD', 'Testing', 'Problem Solving'],
 ARRAY['Electric Vehicles', 'Safety Systems'], 'mid',
 500000, 1000000, 'INR', 'Chennai', false, 'urban', 'balanced', 0.7, 0.6, 0.6, 0.7, 0.8, 0.7, 0.4, 'growing', 0.79, true),

('Electronics Engineer', 'Engineering', 'Design electronic circuits and systems',
 ARRAY['Electronics', 'Circuit Design', 'Programming', 'Problem Solving'],
 ARRAY['Embedded Systems', 'IoT', 'Signal Processing'], 'entry',
 350000, 750000, 'INR', 'Multiple Cities', false, 'urban', 'modern', 0.7, 0.7, 0.7, 0.7, 0.8, 0.7, 0.3, 'growing', 0.80, true),

('Quality Engineer', 'Engineering', 'Ensure products meet quality standards and specifications',
 ARRAY['Quality Control', 'Testing', 'Process Improvement', 'Attention to Detail'],
 ARRAY['Six Sigma', 'Statistical Analysis'], 'mid',
 400000, 800000, 'INR', 'Multiple Cities', false, 'urban', 'balanced', 0.8, 0.7, 0.7, 0.8, 0.7, 0.8, 0.3, 'stable', 0.79, true),

-- Creative & Media (10 opportunities)  
('Graphic Designer', 'Creative', 'Create visual concepts and designs for various media',
 ARRAY['Design', 'Creativity', 'Adobe Creative Suite', 'Visual Communication'],
 ARRAY['Branding', 'Web Design', 'Animation'], 'entry',
 250000, 600000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.7, 0.8, 0.6, 0.4, 'growing', 0.78, true),

('Content Writer', 'Creative', 'Create written content for websites, blogs, and marketing',
 ARRAY['Writing', 'Communication', 'Research', 'Creativity'],
 ARRAY['SEO Writing', 'Technical Writing', 'Copywriting'], 'entry',
 200000, 500000, 'INR', 'Multiple Cities', true, 'both', 'modern', 0.8, 0.8, 0.9, 0.7, 0.7, 0.6, 0.3, 'growing', 0.77, true),

('Video Editor', 'Creative', 'Edit and produce video content for various platforms',
 ARRAY['Video Editing', 'Creativity', 'Software Skills', 'Storytelling'],
 ARRAY['Motion Graphics', 'Color Grading', 'Sound Design'], 'entry',
 300000, 700000, 'INR', 'Mumbai', true, 'urban', 'modern', 0.7, 0.7, 0.8, 0.7, 0.8, 0.6, 0.3, 'booming', 0.78, true),

('Photographer', 'Creative', 'Capture and create professional photographs',
 ARRAY['Photography', 'Creativity', 'Visual Composition', 'Photo Editing'],
 ARRAY['Wedding Photography', 'Commercial Photography'], 'entry',
 150000, 800000, 'INR', 'All India', true, 'both', 'modern', 0.8, 0.7, 0.8, 0.7, 0.7, 0.5, 0.4, 'stable', 0.74, true),

('Social Media Manager', 'Creative', 'Manage social media presence and digital marketing',
 ARRAY['Social Media', 'Communication', 'Marketing', 'Creativity'],
 ARRAY['Analytics', 'Content Creation', 'Community Management'], 'entry',
 250000, 600000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.7, 0.8, 0.6, 0.3, 'booming', 0.79, true),

('Interior Designer', 'Creative', 'Design interior spaces for homes and commercial properties',
 ARRAY['Design', 'Creativity', 'Space Planning', 'Client Communication'],
 ARRAY['3D Modeling', 'Project Management'], 'entry',
 200000, 800000, 'INR', 'Multiple Cities', false, 'urban', 'modern', 0.8, 0.6, 0.7, 0.8, 0.8, 0.7, 0.2, 'growing', 0.79, true),

('Fashion Designer', 'Creative', 'Design clothing and fashion accessories',
 ARRAY['Fashion Design', 'Creativity', 'Drawing', 'Trend Analysis'],
 ARRAY['Pattern Making', 'Textile Knowledge'], 'entry',
 150000, 1000000, 'INR', 'Mumbai', false, 'urban', 'modern', 0.7, 0.6, 0.7, 0.7, 0.8, 0.5, 0.4, 'stable', 0.73, true),

('Game Designer', 'Creative', 'Design and develop video games and interactive experiences',
 ARRAY['Game Design', 'Creativity', 'Programming', 'Storytelling'],
 ARRAY['Unity', 'User Experience', '3D Modeling'], 'mid',
 400000, 1000000, 'INR', 'Bangalore', true, 'urban', 'modern', 0.6, 0.6, 0.8, 0.6, 0.9, 0.7, 0.3, 'booming', 0.77, true),

('Animator', 'Creative', 'Create animated content for films, games, and media',
 ARRAY['Animation', 'Creativity', 'Software Skills', 'Storytelling'],
 ARRAY['3D Animation', 'Motion Graphics', 'Character Design'], 'entry',
 300000, 800000, 'INR', 'Mumbai', true, 'urban', 'modern', 0.7, 0.6, 0.8, 0.6, 0.8, 0.6, 0.3, 'growing', 0.76, true),

('Digital Marketing Specialist', 'Creative', 'Plan and execute digital marketing campaigns',
 ARRAY['Digital Marketing', 'Analytics', 'Communication', 'Strategy'],
 ARRAY['Google Ads', 'Facebook Marketing', 'Email Marketing'], 'entry',
 300000, 700000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.7, 0.9, 0.7, 0.8, 0.7, 0.3, 'booming', 0.81, true),

-- Government & Public Service (10 opportunities)
('IAS Officer', 'Government', 'Serve as administrative officer in government departments',
 ARRAY['Leadership', 'Public Administration', 'Communication', 'Policy Analysis'],
 ARRAY['Governance', 'Rural Development'], 'senior',
 500000, 1200000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.5, 0.9, 0.7, 0.9, 0.1, 'stable', 0.88, true),

('Police Officer', 'Government', 'Maintain law and order and ensure public safety',
 ARRAY['Law Enforcement', 'Physical Fitness', 'Communication', 'Problem Solving'],
 ARRAY['Investigation', 'Crime Prevention'], 'entry',
 300000, 700000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.6, 0.9, 0.7, 0.8, 0.1, 'stable', 0.86, true),

('Government Teacher', 'Government', 'Teach in government-run educational institutions',
 ARRAY['Teaching', 'Subject Knowledge', 'Communication', 'Patience'],
 ARRAY['Curriculum Development', 'Educational Technology'], 'entry',
 250000, 600000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.9, 0.6, 0.9, 0.1, 'stable', 0.87, true),

('Bank Clerk (Government)', 'Government', 'Handle banking operations in public sector banks',
 ARRAY['Banking Operations', 'Customer Service', 'Attention to Detail', 'Communication'],
 ARRAY['Computer Skills', 'Financial Products'], 'entry',
 250000, 500000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.8, 0.6, 0.8, 0.3, 'stable', 0.83, true),

('Railway Officer', 'Government', 'Manage railway operations and administration',
 ARRAY['Administration', 'Safety Management', 'Communication', 'Leadership'],
 ARRAY['Transportation Planning', 'Operations Management'], 'mid',
 400000, 800000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.8, 0.6, 0.8, 0.7, 0.8, 0.2, 'stable', 0.82, true),

('Defense Officer', 'Government', 'Serve in Indian Armed Forces in various capacities',
 ARRAY['Leadership', 'Physical Fitness', 'Discipline', 'Strategic Thinking'],
 ARRAY['Military Strategy', 'Team Management'], 'entry',
 400000, 900000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.7, 0.4, 0.9, 0.8, 0.9, 0.1, 'stable', 0.84, true),

('Municipal Officer', 'Government', 'Manage local government administration and services',
 ARRAY['Public Administration', 'Communication', 'Problem Solving', 'Leadership'],
 ARRAY['Urban Planning', 'Public Service'], 'mid',
 300000, 700000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.6, 0.8, 0.7, 0.8, 0.1, 'stable', 0.83, true),

('Forest Officer', 'Government', 'Protect and manage forest resources and wildlife',
 ARRAY['Environmental Science', 'Forest Management', 'Physical Fitness', 'Leadership'],
 ARRAY['Wildlife Conservation', 'Ecology'], 'mid',
 350000, 700000, 'INR', 'All India', false, 'rural', 'traditional', 0.8, 0.7, 0.5, 0.8, 0.9, 0.8, 0.1, 'growing', 0.81, true),

('Custom Officer', 'Government', 'Manage import/export procedures and customs regulations',
 ARRAY['Customs Law', 'Investigation', 'Communication', 'Attention to Detail'],
 ARRAY['International Trade', 'Risk Assessment'], 'mid',
 400000, 800000, 'INR', 'Port Cities', false, 'urban', 'traditional', 0.8, 0.7, 0.6, 0.8, 0.7, 0.8, 0.2, 'stable', 0.81, true),

('Public Health Officer', 'Government', 'Manage public health programs and disease prevention',
 ARRAY['Public Health', 'Healthcare Management', 'Communication', 'Data Analysis'],
 ARRAY['Epidemiology', 'Health Policy'], 'mid',
 350000, 750000, 'INR', 'All India', false, 'both', 'traditional', 0.9, 0.8, 0.7, 0.8, 0.8, 0.8, 0.1, 'growing', 0.85, true),

-- Agriculture & Environment (10 opportunities)
('Agricultural Scientist', 'Agriculture', 'Research and develop agricultural technologies and practices',
 ARRAY['Agricultural Science', 'Research', 'Problem Solving', 'Data Analysis'],
 ARRAY['Crop Science', 'Soil Science', 'Plant Pathology'], 'senior',
 400000, 800000, 'INR', 'Rural Areas', false, 'rural', 'traditional', 0.8, 0.7, 0.5, 0.8, 0.8, 0.8, 0.2, 'growing', 0.82, true),

('Veterinarian', 'Agriculture', 'Provide medical care for animals and livestock',
 ARRAY['Veterinary Medicine', 'Animal Care', 'Communication', 'Problem Solving'],
 ARRAY['Large Animal Care', 'Surgery', 'Preventive Medicine'], 'senior',
 300000, 800000, 'INR', 'All India', false, 'both', 'traditional', 0.8, 0.7, 0.6, 0.8, 0.8, 0.8, 0.1, 'stable', 0.83, true),

('Agricultural Engineer', 'Agriculture', 'Design agricultural machinery and irrigation systems',
 ARRAY['Agricultural Engineering', 'Mechanical Design', 'Problem Solving'],
 ARRAY['Irrigation Systems', 'Farm Machinery'], 'mid',
 350000, 700000, 'INR', 'Rural Areas', false, 'rural', 'traditional', 0.8, 0.7, 0.5, 0.7, 0.8, 0.7, 0.3, 'growing', 0.79, true),

('Farm Manager', 'Agriculture', 'Manage agricultural operations and farm productivity',
 ARRAY['Farm Management', 'Agriculture', 'Leadership', 'Business Management'],
 ARRAY['Crop Planning', 'Livestock Management'], 'mid',
 250000, 600000, 'INR', 'Rural Areas', false, 'rural', 'traditional', 0.9, 0.8, 0.5, 0.8, 0.7, 0.7, 0.3, 'stable', 0.80, true),

('Food Technologist', 'Agriculture', 'Develop and improve food products and processing methods',
 ARRAY['Food Science', 'Quality Control', 'Research', 'Problem Solving'],
 ARRAY['Food Safety', 'Product Development'], 'mid',
 350000, 750000, 'INR', 'Multiple Cities', false, 'urban', 'balanced', 0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.2, 'growing', 0.79, true),

('Environmental Consultant', 'Environment', 'Advise on environmental compliance and sustainability',
 ARRAY['Environmental Science', 'Consulting', 'Problem Solving', 'Communication'],
 ARRAY['Environmental Impact Assessment', 'Sustainability'], 'mid',
 400000, 900000, 'INR', 'Multiple Cities', true, 'urban', 'modern', 0.8, 0.6, 0.8, 0.7, 0.9, 0.8, 0.1, 'booming', 0.84, true),

('Wildlife Conservationist', 'Environment', 'Protect wildlife and natural habitats',
 ARRAY['Wildlife Biology', 'Conservation', 'Research', 'Communication'],
 ARRAY['Field Research', 'Habitat Management'], 'mid',
 250000, 600000, 'INR', 'Rural Areas', false, 'rural', 'modern', 0.7, 0.7, 0.5, 0.7, 0.9, 0.8, 0.1, 'growing', 0.80, true),

('Renewable Energy Technician', 'Environment', 'Install and maintain renewable energy systems',
 ARRAY['Technical Skills', 'Problem Solving', 'Safety', 'Electrical Knowledge'],
 ARRAY['Solar Energy', 'Wind Energy'], 'entry',
 250000, 550000, 'INR', 'All India', false, 'both', 'modern', 0.7, 0.7, 0.7, 0.7, 0.9, 0.8, 0.2, 'booming', 0.81, true),

('Water Resource Engineer', 'Environment', 'Design water management and conservation systems',
 ARRAY['Water Engineering', 'Environmental Science', 'Problem Solving', 'Design'],
 ARRAY['Hydrology', 'Water Treatment'], 'mid',
 400000, 900000, 'INR', 'Multiple Cities', false, 'both', 'balanced', 0.8, 0.7, 0.6, 0.7, 0.9, 0.8, 0.2, 'growing', 0.82, true),

('Organic Farming Specialist', 'Agriculture', 'Promote and implement organic farming practices',
 ARRAY['Organic Agriculture', 'Sustainability', 'Communication', 'Training'],
 ARRAY['Soil Health', 'Pest Management'], 'mid',
 200000, 500000, 'INR', 'Rural Areas', false, 'rural', 'modern', 0.8, 0.8, 0.6, 0.8, 0.8, 0.7, 0.2, 'growing', 0.82, true);

-- Add indexes and update statistics
ANALYZE career_opportunities;

-- Create additional helpful views for the MARE system
CREATE OR REPLACE VIEW mare_career_summary AS
SELECT 
    id,
    title,
    industry,
    salary_range_min,
    salary_range_max,
    urban_rural_suitability,
    growth_potential_score,
    job_security_score,
    future_outlook,
    mare_compatibility_score,
    COUNT(*) OVER() as total_careers
FROM career_opportunities 
WHERE is_active = true;

-- Grant necessary permissions (adjust as needed for your setup)
-- GRANT SELECT ON career_opportunities TO authenticated;
-- GRANT SELECT ON mare_career_summary TO authenticated;

-- Final count and verification
SELECT 
    COUNT(*) as total_careers,
    COUNT(DISTINCT industry) as industries,
    AVG(salary_range_min) as avg_min_salary,
    AVG(salary_range_max) as avg_max_salary,
    COUNT(CASE WHEN remote_available THEN 1 END) as remote_jobs,
    COUNT(CASE WHEN urban_rural_suitability = 'both' THEN 1 END) as flexible_location_jobs
FROM career_opportunities;
