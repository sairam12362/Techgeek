import streamlit as st
import os
import json
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Skill:
    name: str
    category: str
    proficiency: str
    confidence: float


@dataclass
class ResumeScore:
    overall_score: float
    sections: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    ats_score: float


@dataclass
class CareerRecommendation:
    job_title: str
    match_score: float
    required_skills: List[str]
    missing_skills: List[str]
    salary_range: str
    growth_potential: str
    job_description: str


class AIResumeAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.tech_skills_db = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php'],
            'web_dev': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'express'],
            'data_science': ['machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'databases': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'],
            'tools': ['git', 'jira', 'slack', 'vscode', 'intellij', 'postman']
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'project management', 'time management', 'collaboration', 'adaptability', 'creativity'
        ]
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, file_path: str) -> str:
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_skills(self, text: str) -> List[Skill]:
        text_lower = text.lower()
        skills = []
        
        for category, skill_list in self.tech_skills_db.items():
            for skill in skill_list:
                if skill in text_lower:
                    confidence = min(text_lower.count(skill) * 0.2, 1.0)
                    skills.append(Skill(
                        name=skill,
                        category=category,
                        proficiency='Intermediate',
                        confidence=confidence
                    ))
        
        for skill in self.soft_skills:
            if skill in text_lower:
                confidence = min(text_lower.count(skill) * 0.15, 1.0)
                skills.append(Skill(
                    name=skill,
                    category='Soft Skills',
                    proficiency='Intermediate',
                    confidence=confidence
                ))
        
        return skills
    
    def analyze_with_ai(self, text: str, skills: List[Skill]) -> Dict[str, Any]:
        if not self.api_key:
            return self._mock_ai_analysis(text, skills)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""
            Analyze this resume text and provide detailed feedback:
            
            Resume Text:
            {text[:2000]}
            
            Skills Found: {[skill.name for skill in skills]}
            
            Please provide:
            1. Overall score (0-100)
            2. ATS compatibility score (0-100)
            3. Key strengths (3-5 points)
            4. Areas for improvement (3-5 points)
            5. Specific recommendations (3-5 points)
            6. Section scores: contact_info, summary, experience, education, skills
            
            Format as JSON.
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            return self._mock_ai_analysis(text, skills)
    
    def _mock_ai_analysis(self, text: str, skills: List[Skill]) -> Dict[str, Any]:
        word_count = len(text.split())
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
        
        base_score = 40
        if has_email: base_score += 10
        if has_phone: base_score += 10
        if word_count >= 200: base_score += 15
        if len(skills) >= 5: base_score += 15
        if 'experience' in text.lower(): base_score += 10
        
        return {
            "overall_score": min(base_score, 100),
            "ats_score": min(base_score - 5, 95),
            "strengths": [
                "Clear contact information" if has_email else "Professional formatting",
                "Good skill representation" if len(skills) >= 5 else "Concise content",
                "Relevant experience section" if 'experience' in text.lower() else "Educational background"
            ],
            "weaknesses": [
                "Missing phone number" if not has_phone else "Could be more detailed",
                "Limited skill keywords" if len(skills) < 5 else "Needs quantifiable achievements",
                "ATS optimization needed"
            ],
            "recommendations": [
                "Add quantifiable achievements",
                "Include more industry-specific keywords",
                "Optimize for ATS systems",
                "Add professional summary",
                "Include portfolio links if applicable"
            ],
            "sections": {
                "contact_info": 100 if (has_email and has_phone) else 50,
                "summary": 80 if word_count >= 50 else 60,
                "experience": 85 if 'experience' in text.lower() else 40,
                "education": 75 if 'education' in text.lower() else 50,
                "skills": 90 if len(skills) >= 5 else 60
            }
        }
    
    def generate_career_recommendations(self, skills: List[Skill]) -> List[CareerRecommendation]:
        skill_names = [skill.name.lower() for skill in skills]
        
        career_paths = [
            {
                "job_title": "Software Engineer",
                "required_skills": ["python", "javascript", "git", "sql", "problem solving"],
                "salary_range": "$70k - $150k",
                "growth_potential": "High",
                "description": "Develop and maintain software applications, collaborate with cross-functional teams, and participate in the full software development lifecycle."
            },
            {
                "job_title": "Data Scientist",
                "required_skills": ["python", "machine learning", "data science", "sql", "statistics"],
                "salary_range": "$80k - $160k",
                "growth_potential": "Very High",
                "description": "Analyze complex datasets, build machine learning models, and provide data-driven insights to drive business decisions."
            },
            {
                "job_title": "Product Manager",
                "required_skills": ["project management", "communication", "leadership", "analytical"],
                "salary_range": "$75k - $140k",
                "growth_potential": "High",
                "description": "Lead product development, coordinate between teams, and drive product strategy based on market research and user feedback."
            },
            {
                "job_title": "Full Stack Developer",
                "required_skills": ["javascript", "react", "node.js", "sql", "html"],
                "salary_range": "$65k - $130k",
                "growth_potential": "High",
                "description": "Build end-to-end web applications, manage both frontend and backend development, and ensure seamless user experiences."
            },
            {
                "job_title": "DevOps Engineer",
                "required_skills": ["docker", "kubernetes", "aws", "git", "linux"],
                "salary_range": "$75k - $145k",
                "growth_potential": "Very High",
                "description": "Automate deployment processes, manage cloud infrastructure, and ensure system reliability and scalability."
            }
        ]
        
        recommendations = []
        for career in career_paths:
            required = career["required_skills"]
            match_count = sum(1 for skill in required if skill in skill_names)
            match_score = (match_count / len(required)) * 100
            
            missing = [skill for skill in required if skill not in skill_names]
            
            recommendations.append(CareerRecommendation(
                job_title=career["job_title"],
                match_score=match_score,
                required_skills=required,
                missing_skills=missing,
                salary_range=career["salary_range"],
                growth_potential=career["growth_potential"],
                job_description=career["description"]
            ))
        
        return sorted(recommendations, key=lambda x: x.match_score, reverse=True)


def create_realistic_ui():
    st.set_page_config(
        page_title="VidyāMitra - AI Career Agent",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Professional CSS with Enhanced Interactivity
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-left-width: 6px;
        }
        
        .metric-card h3 {
            color: #2c3e50;
            font-weight: 600;
            margin: 0;
            transition: color 0.3s ease;
        }
        
        .metric-card:hover h3 {
            color: #667eea;
        }
        
        .metric-card p {
            color: #7f8c8d;
            margin: 0;
            font-size: 0.9rem;
        }
        
        .skill-tag {
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.9rem;
            font-weight: 500;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .skill-tag::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .skill-tag:hover::before {
            left: 100%;
        }
        
        .skill-tag:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .career-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #28a745;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .career-card:hover {
            transform: translateX(10px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            border-left-width: 6px;
        }
        
        .career-card h3 {
            color: #2c3e50;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        
        .career-card:hover h3 {
            color: #28a745;
        }
        
        .career-card p {
            color: #5a6c7d;
            line-height: 1.6;
        }
        
        .recommendation-box {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .recommendation-box:hover {
            background: #fff3cd;
            transform: translateX(5px);
            box-shadow: 0 2px 10px rgba(255, 193, 7, 0.2);
        }
        
        .recommendation-box strong {
            color: #2c3e50;
        }
        
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
            position: relative;
            overflow: hidden;
        }
        
        .stProgress > div > div > div > div::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: progress-shimmer 2s infinite;
        }
        
        @keyframes progress-shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 0.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #5a6c7d;
            font-weight: 500;
            transition: all 0.3s ease;
            border-radius: 6px;
            position: relative;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e9ecef;
            transform: translateY(-1px);
        }
        
        .stTabs [aria-selected="true"] {
            color: #667eea;
            background-color: white;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            position: relative;
        }
        
        h1::after, h2::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s ease;
        }
        
        h1:hover::after, h2:hover::after {
            width: 100%;
        }
        
        .stSelectbox > div > div {
            background-color: white;
            color: #2c3e50;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .stFileUploader > div > div {
            background-color: white;
            border: 2px dashed #667eea;
            border-radius: 8px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .stFileUploader > div > div:hover {
            border-color: #764ba2;
            background-color: #f8f9ff;
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        }
        
        .stFileUploader > div > div::before {
            content: '📁';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3rem;
            opacity: 0.1;
            transition: opacity 0.3s ease;
        }
        
        .stFileUploader > div > div:hover::before {
            opacity: 0.2;
        }
        
        .stAlert {
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .stAlert:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .stSpinner > div {
            color: #667eea;
        }
        
        .stMetric {
            background-color: white;
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stMetric::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .stMetric:hover::before {
            left: 100%;
        }
        
        .stMetric:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .stMetric label {
            color: #5a6c7d;
            font-weight: 500;
        }
        
        .stMetric div {
            color: #2c3e50;
            font-weight: 600;
        }
        
        .animated-number {
            animation: countUp 1s ease-out;
        }
        
        @keyframes countUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 VidyāMitra</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-Powered Resume Evaluator, Trainer & Career Planner</p>
        <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">Advanced AI Analysis • Career Matching • Skill Development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = AIResumeAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Sidebar
    st.sidebar.markdown("### 📁 Upload Resume")
    uploaded_file = st.sidebar.file_uploader(
        "Choose your resume",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    # AI Status
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        st.sidebar.success("✅ AI Analysis Enabled")
    else:
        st.sidebar.warning("⚠️ AI Analysis Disabled (No API Key)")
        st.sidebar.info("Add OPENAI_API_KEY to .env file for enhanced analysis")
    
    # Process uploaded file
    if uploaded_file and st.session_state.analysis_result is None:
        with st.spinner("🤖 AI analyzing your resume..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Extract text
                file_extension = Path(uploaded_file.name).suffix.lower()
                if file_extension == '.pdf':
                    text = analyzer.extract_text_from_pdf(tmp_file_path)
                elif file_extension == '.docx':
                    text = analyzer.extract_text_from_docx(tmp_file_path)
                elif file_extension == '.txt':
                    text = open(tmp_file_path, 'r', encoding='utf-8').read()
                else:
                    text = "Unsupported file format"
                
                # Extract skills
                skills = analyzer.extract_skills(text)
                
                # AI Analysis
                ai_analysis = analyzer.analyze_with_ai(text, skills)
                
                # Career recommendations
                career_recommendations = analyzer.generate_career_recommendations(skills)
                
                # Create resume score object
                resume_score = ResumeScore(
                    overall_score=ai_analysis['overall_score'],
                    sections=ai_analysis['sections'],
                    strengths=ai_analysis['strengths'],
                    weaknesses=ai_analysis['weaknesses'],
                    recommendations=ai_analysis['recommendations'],
                    ats_score=ai_analysis['ats_score']
                )
                
                # Store results
                st.session_state.analysis_result = {
                    'text': text,
                    'skills': skills,
                    'score': resume_score,
                    'career_recommendations': career_recommendations,
                    'file_info': {
                        'name': uploaded_file.name,
                        'size': uploaded_file.size,
                        'type': uploaded_file.type
                    },
                    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Clean up
                os.unlink(tmp_file_path)
                
                st.success("✅ AI Analysis Complete!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                return
    
    # Display results
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        
        # Key Metrics Row with Enhanced Interactivity
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card animated-number">
                <h3 style="margin: 0; color: #667eea;" class="pulse">{result['score'].overall_score:.0f}</h3>
                <p style="margin: 0; font-size: 0.9rem;">Overall Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card animated-number" style="animation-delay: 0.1s;">
                <h3 style="margin: 0; color: #28a745;" class="pulse">{result['score'].ats_score:.0f}</h3>
                <p style="margin: 0; font-size: 0.9rem;">ATS Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card animated-number" style="animation-delay: 0.2s;">
                <h3 style="margin: 0; color: #ffc107;" class="pulse">{len(result['skills'])}</h3>
                <p style="margin: 0; font-size: 0.9rem;">Skills Found</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            word_count = len(result['text'].split())
            st.markdown(f"""
            <div class="metric-card animated-number" style="animation-delay: 0.3s;">
                <h3 style="margin: 0; color: #17a2b8;" class="pulse">{word_count}</h3>
                <p style="margin: 0; font-size: 0.9rem;">Word Count</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card animated-number" style="animation-delay: 0.4s;">
                <h3 style="margin: 0; color: #dc3545;" class="pulse">{result['analysis_time']}</h3>
                <p style="margin: 0; font-size: 0.9rem;">Analyzed</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Analysis", "💼 Skills", "🎯 Careers", "📈 ATS Score", "💡 Recommendations"
        ])
        
        with tab1:
            st.header("📊 Resume Analysis")
            
            # Score Breakdown
            st.subheader("Score Breakdown")
            for section, score in result['score'].sections.items():
                st.write(f"**{section.replace('_', ' ').title()}:** {score:.0f}/100")
                st.progress(score / 100)
            
            # Strengths and Weaknesses
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Strengths")
                for strength in result['score'].strengths:
                    st.markdown(f"""
                    <div class="recommendation-box">
                        <strong>✓</strong> {strength}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("⚠️ Areas for Improvement")
                for weakness in result['score'].weaknesses:
                    st.markdown(f"""
                    <div class="recommendation-box">
                        <strong>!</strong> {weakness}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            st.header("💼 Skills Analysis")
            
            # Group skills by category
            skills_by_category = {}
            for skill in result['skills']:
                if skill.category not in skills_by_category:
                    skills_by_category[skill.category] = []
                skills_by_category[skill.category].append(skill)
            
            for category, skills in skills_by_category.items():
                st.subheader(f"🔹 {category.title()}")
                for i, skill in enumerate(skills):
                    confidence_percent = skill.confidence * 100
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0;">
                        <span class="skill-tag slide-in" style="animation-delay: {i * 0.1}s;" 
                              onclick="this.style.transform='scale(1.1)'; setTimeout(() => this.style.transform='scale(1)', 200);"
                              title="Click to highlight!">{skill.name}</span>
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">{confidence_percent:.0f}% confidence</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            st.header("🎯 Career Recommendations")
            
            recommendations = result['career_recommendations'][:5]
            for i, rec in enumerate(recommendations):
                match_color = "#28a745" if rec.match_score >= 70 else "#ffc107" if rec.match_score >= 50 else "#dc3545"
                
                required_skills_tags = ', '.join([f'<span class="skill-tag" style="font-size: 0.8rem; padding: 0.3rem 0.6rem;">{skill}</span>' for skill in rec.required_skills])
                
                missing_skills_html = ""
                if rec.missing_skills:
                    missing_skills_tags = ', '.join([f'<span class="skill-tag" style="font-size: 0.8rem; padding: 0.3rem 0.6rem; background: linear-gradient(45deg, #dc3545, #ffc107);">{skill}</span>' for skill in rec.missing_skills])
                    missing_skills_html = f'<div style="margin: 1rem 0;"><strong>Missing Skills:</strong><br><div style="margin-top: 0.5rem;">{missing_skills_tags}</div></div>'
                
                st.markdown(f"""
                <div class="career-card slide-in" style="animation-delay: {i * 0.2}s;" 
                     onmouseover="this.style.transform='translateX(15px) scale(1.02)';"
                     onmouseout="this.style.transform='translateX(0) scale(1)';">
                    <h3 style="color: {match_color}; margin: 0;">{rec.job_title}</h3>
                    <p style="color: #666; margin: 0.5rem 0;">{rec.job_description}</p>
                    
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <strong>Match Score:</strong> 
                        <span style="color: {match_color}; font-weight: 600; font-size: 1.1rem;">{rec.match_score:.0f}%</span>
                        <strong>Salary:</strong> <span style="font-weight: 500;">{rec.salary_range}</span>
                        <strong>Growth:</strong> <span style="font-weight: 500;">{rec.growth_potential}</span>
                    </div>
                    
                    <div style="margin: 1rem 0;">
                        <strong>Required Skills:</strong><br>
                        <div style="margin-top: 0.5rem;">
                            {required_skills_tags}
                        </div>
                    </div>
                    
                    {missing_skills_html}
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.header("📈 ATS Optimization Score")
            
            ats_score = result['score'].ats_score
            ats_color = "#28a745" if ats_score >= 80 else "#ffc107" if ats_score >= 60 else "#dc3545"
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; font-size: 2rem;">
                <div style="color: {ats_color};">{ats_score:.0f}/100</div>
                <div style="font-size: 1rem; color: #666;">ATS Compatibility Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("ATS Optimization Tips")
            tips = [
                "Use standard section headers (Experience, Education, Skills)",
                "Include relevant keywords from job descriptions",
                "Avoid tables, columns, and complex formatting",
                "Use standard fonts (Arial, Calibri, Times New Roman)",
                "Save as .docx or plain text for best ATS compatibility",
                "Include both acronyms and full terms (e.g., 'AI' and 'Artificial Intelligence')"
            ]
            
            for tip in tips:
                st.markdown(f"""
                <div class="recommendation-box">
                    <strong>💡</strong> {tip}
                </div>
                """, unsafe_allow_html=True)
        
        with tab5:
            st.header("💡 Improvement Recommendations")
            
            for i, rec in enumerate(result['score'].recommendations, 1):
                st.markdown(f"""
                <div class="recommendation-box">
                    <h4>{i}. {rec}</h4>
                </div>
                """, unsafe_allow_html=True)
        
        # Reset button
        if st.sidebar.button("🔄 Analyze New Resume"):
            st.session_state.analysis_result = None
            st.rerun()
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #667eea;">Welcome to VidyāMitra! 🎯</h2>
            <p style="font-size: 1.1rem; color: #666; margin: 1rem 0;">
                Your AI-powered career companion is ready to transform your resume into a powerful career tool
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #667eea; margin: 0;">🤖 AI Analysis</h3>
                    <p style="color: #666; margin: 0.5rem 0;">Advanced AI-powered resume evaluation</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #28a745; margin: 0;">📊 ATS Score</h3>
                    <p style="color: #666; margin: 0.5rem 0;">Optimize for automated screening</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #ffc107; margin: 0;">🎯 Career Matching</h3>
                    <p style="color: #666; margin: 0.5rem 0;">Personalized job recommendations</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #17a2b8; margin: 0;">💡 Smart Insights</h3>
                    <p style="color: #666; margin: 0.5rem 0;">Actionable improvement tips</p>
                </div>
            </div>
            
            <h3 style="color: #667eea; margin-top: 2rem;">Ready to get started?</h3>
            <p style="font-size: 1.1rem; color: #666;">
                <strong>Upload your resume in the sidebar to begin your AI-powered career analysis!</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    create_realistic_ui()
