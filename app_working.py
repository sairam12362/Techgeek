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


@dataclass
class Skill:
    name: str
    category: str
    proficiency: str


@dataclass
class ResumeScore:
    overall_score: float
    sections: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


@dataclass
class CareerRecommendation:
    job_title: str
    match_score: float
    required_skills: List[str]
    missing_skills: List[str]
    salary_range: str
    growth_potential: str


class UserAuth:
    def __init__(self):
        self.users_file = "users.json"
        self.sessions_file = "sessions.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if email in users:
                return {"success": False, "message": "User already exists"}
            
            users[email] = {
                "password": self._hash_password(password),
                "name": name,
                "created_at": datetime.now().isoformat(),
                "profile": {
                    "skills": [],
                    "experience": "",
                    "career_goals": "",
                    "resume_analyses": []
                }
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return {"success": True, "message": "User registered successfully"}
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if email not in users:
                return {"success": False, "message": "User not found"}
            
            if users[email]["password"] != self._hash_password(password):
                return {"success": False, "message": "Invalid password"}
            
            session_id = hashlib.sha256(f"{email}{datetime.now()}".encode()).hexdigest()
            session_data = {
                "email": email,
                "name": users[email]["name"],
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            sessions[session_id] = session_data
            
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            
            return {
                "success": True,
                "message": "Login successful",
                "session_id": session_id,
                "user": {
                    "email": email,
                    "name": users[email]["name"],
                    "profile": users[email]["profile"]
                }
            }
        except Exception as e:
            return {"success": False, "message": f"Login failed: {str(e)}"}


class TrainingResourceManager:
    def __init__(self):
        self.resources_db = self._initialize_resources()
    
    def _initialize_resources(self) -> Dict[str, List[Dict]]:
        resources = {
            'python': [
                {
                    "title": "Python for Everybody",
                    "provider": "Coursera",
                    "type": "course",
                    "duration": "8 weeks",
                    "difficulty": "Beginner",
                    "url": "https://www.coursera.org/specializations/python",
                    "rating": 4.8,
                    "cost": "Free (with certificate)",
                    "skills_covered": ["python", "programming", "data structures"]
                }
            ],
            'javascript': [
                {
                    "title": "JavaScript: The Complete Guide",
                    "provider": "Udemy",
                    "type": "course",
                    "duration": "27 hours",
                    "difficulty": "Beginner",
                    "url": "https://www.udemy.com/course/javascript-the-complete-guide/",
                    "rating": 4.7,
                    "cost": "$19.99",
                    "skills_covered": ["javascript", "web development", "es6"]
                }
            ]
        }
        return resources
    
    def get_resources_for_skill(self, skill_name: str) -> List[Dict]:
        skill_key = skill_name.lower()
        
        if skill_key in self.resources_db:
            return self.resources_db[skill_key]
        
        for key in self.resources_db:
            if skill_key in key or key in skill_key:
                return self.resources_db[key]
        
        return self._get_general_resources()
    
    def _get_general_resources(self) -> List[Dict]:
        return [
            {
                "title": "LinkedIn Learning",
                "provider": "LinkedIn",
                "type": "course",
                "duration": "Varies",
                "difficulty": "All levels",
                "url": "https://www.linkedin.com/learning/",
                "rating": 4.5,
                "cost": "Subscription",
                "skills_covered": ["business", "technology", "creative"]
            }
        ]


class SimpleResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        self.tech_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning',
            'data science', 'tensorflow', 'pytorch', 'html', 'css', 'angular',
            'vue.js', 'flask', 'django', 'postgresql', 'mysql', 'redis'
        ]
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'critical thinking', 'project management', 'time management',
            'collaboration', 'adaptability', 'creativity', 'analytical'
        ]
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
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
        """Extract text from DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading TXT: {str(e)}"
    
    def extract_skills(self, text: str) -> List[Skill]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        skills = []
        
        for skill in self.tech_skills:
            if skill in text_lower:
                skills.append(Skill(
                    name=skill,
                    category='Technical',
                    proficiency='Intermediate'
                ))
        
        for skill in self.soft_skills:
            if skill in text_lower:
                skills.append(Skill(
                    name=skill,
                    category='Soft Skills',
                    proficiency='Intermediate'
                ))
        
        return skills
    
    def evaluate_resume(self, text: str, skills: List[Skill]) -> ResumeScore:
        """Evaluate resume and give score"""
        scores = {}
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Contact info (20%)
        email_found = bool(re.search(self.email_pattern, text))
        phone_found = bool(re.search(self.phone_pattern, text))
        contact_score = (10 if email_found else 0) + (10 if phone_found else 0)
        scores['contact_info'] = contact_score
        
        # Skills (25%)
        skills_score = min(len(skills) * 2, 25)
        scores['skills'] = skills_score
        
        # Length/Content (30%)
        word_count = len(text.split())
        content_score = min(word_count / 20, 30)  # 1 point per 20 words, max 30
        scores['content'] = content_score
        
        # Structure (25%)
        structure_keywords = ['experience', 'education', 'skills', 'projects']
        structure_score = min(sum(10 for keyword in structure_keywords if keyword.lower() in text.lower()), 25)
        scores['structure'] = structure_score
        
        overall_score = sum(scores.values())
        
        # Generate insights
        if email_found and phone_found:
            strengths.append("Complete contact information provided")
        else:
            weaknesses.append("Missing contact information")
            recommendations.append("Add email and phone number")
        
        if skills_score >= 20:
            strengths.append("Good variety of skills listed")
        else:
            weaknesses.append("Limited skills section")
            recommendations.append("Add more relevant skills")
        
        if word_count >= 200:
            strengths.append("Comprehensive resume content")
        else:
            weaknesses.append("Resume content seems brief")
            recommendations.append("Add more detail about experience and projects")
        
        return ResumeScore(
            overall_score=overall_score,
            sections=scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    def generate_career_recommendations(self, skills: List[Skill]) -> List[CareerRecommendation]:
        career_paths = {
            'Software Engineer': {
                'required_skills': ['python', 'javascript', 'git', 'sql', 'problem solving'],
                'salary_range': '$70k - $150k',
                'growth_potential': 'High'
            },
            'Data Scientist': {
                'required_skills': ['python', 'machine learning', 'data science', 'sql', 'statistics'],
                'salary_range': '$80k - $160k',
                'growth_potential': 'Very High'
            },
            'Product Manager': {
                'required_skills': ['project management', 'communication', 'leadership', 'analytical'],
                'salary_range': '$75k - $140k',
                'growth_potential': 'High'
            }
        }
        
        current_skill_names = [skill.name.lower() for skill in skills]
        recommendations = []
        
        for job_title, job_data in career_paths.items():
            required_skills = job_data['required_skills']
            match_count = sum(1 for skill in required_skills if skill in current_skill_names)
            match_score = (match_count / len(required_skills)) * 100
            
            missing_skills = [skill for skill in required_skills if skill not in current_skill_names]
            
            recommendations.append(CareerRecommendation(
                job_title=job_title,
                match_score=match_score,
                required_skills=required_skills,
                missing_skills=missing_skills,
                salary_range=job_data['salary_range'],
                growth_potential=job_data['growth_potential']
            ))
        
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations


def show_login_page():
    st.title("🔐 Login to VidyāMitra")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if email and password:
                auth = UserAuth()
                result = auth.login_user(email, password)
                
                if result["success"]:
                    st.session_state.session_id = result["session_id"]
                    st.session_state.user = result["user"]
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("Please fill in all fields")
    
    if st.button("Don't have an account? Register"):
        st.session_state.show_register = True
        st.rerun()


def show_register_page():
    st.title("📝 Register for VidyāMitra")
    
    with st.form("register_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    auth = UserAuth()
                    result = auth.register_user(email, password, name)
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(result["message"])
            else:
                st.error("Please fill in all fields")
    
    if st.button("Already have an account? Login"):
        st.session_state.show_register = False
        st.rerun()


def show_profile_page(user):
    st.title(f"👤 {user['name']}'s Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Profile Information")
        
        with st.form("profile_form"):
            skills = st.text_area("Skills", value=", ".join(user['profile'].get('skills', [])), 
                                 help="Enter your skills separated by commas")
            experience = st.text_area("Experience", value=user['profile'].get('experience', ''),
                                    help="Describe your work experience")
            career_goals = st.text_area("Career Goals", value=user['profile'].get('career_goals', ''),
                                       help="What are your career aspirations?")
            
            update_button = st.form_submit_button("Update Profile")
            
            if update_button:
                profile_data = {
                    "skills": [skill.strip() for skill in skills.split(',') if skill.strip()],
                    "experience": experience,
                    "career_goals": career_goals
                }
                
                st.success("Profile updated successfully!")
    
    with col2:
        st.subheader("📊 Statistics")
        
        analyses = user['profile'].get('resume_analyses', [])
        st.metric("Resume Analyses", len(analyses))
        
        skills_count = len(user['profile'].get('skills', []))
        st.metric("Skills Listed", skills_count)


def main():
    st.set_page_config(
        page_title="VidyāMitra - AI Career Agent",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
        }
        .skill-tag {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            margin: 0.2rem;
            font-size: 0.9rem;
        }
        .recommendation-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎯 VidyāMitra</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">AI-Powered Resume Evaluator, Trainer & Career Planner</p>', unsafe_allow_html=True)
    
    # File upload section
    st.sidebar.header("📁 Upload Resume")
    uploaded_file = st.sidebar.file_uploader(
        "Choose your resume",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    # Initialize session state
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    
    # Process uploaded file
    if uploaded_file and st.session_state.analysis_result is None:
        with st.spinner("🔍 Analyzing your resume..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Parse resume
                parser = SimpleResumeParser()
                file_extension = Path(uploaded_file.name).suffix.lower()
                
                if file_extension == '.pdf':
                    text = parser.extract_text_from_pdf(tmp_file_path)
                elif file_extension == '.docx':
                    text = parser.extract_text_from_docx(tmp_file_path)
                elif file_extension == '.txt':
                    text = parser.extract_text_from_txt(tmp_file_path)
                else:
                    text = "Unsupported file format"
                
                # Extract skills and evaluate
                skills = parser.extract_skills(text)
                score = parser.evaluate_resume(text, skills)
                
                # Store results
                st.session_state.analysis_result = {
                    'text': text,
                    'skills': skills,
                    'score': score,
                    'file_info': {
                        'name': uploaded_file.name,
                        'size': uploaded_file.size,
                        'type': uploaded_file.type
                    }
                }
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
                st.success("✅ Resume analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")
                return
    
    # Display results
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        
        # Main dashboard tabs
        tab1, tab2, tab3 = st.tabs(["📈 Overview", "💼 Skills Analysis", "💡 Recommendations"])
        
        with tab1:
            st.header("📈 Resume Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score = result['score'].overall_score
                st.metric("Overall Score", f"{score:.0f}/100")
            
            with col2:
                skills_count = len(result['skills'])
                st.metric("Skills Identified", skills_count)
            
            with col3:
                word_count = len(result['text'].split())
                st.metric("Word Count", word_count)
            
            with col4:
                file_size = result['file_info']['size']
                st.metric("File Size", f"{file_size/1024:.1f} KB")
            
            # Score breakdown
            st.subheader("📊 Score Breakdown")
            sections = result['score'].sections
            
            for section, score_val in sections.items():
                st.write(f"**{section.replace('_', ' ').title()}:** {score_val:.0f}/100")
                st.progress(score_val / 100)
            
            # Strengths and Weaknesses
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Strengths")
                for strength in result['score'].strengths:
                    st.write(f"• {strength}")
            
            with col2:
                st.subheader("⚠️ Areas for Improvement")
                for weakness in result['score'].weaknesses:
                    st.write(f"• {weakness}")
        
        with tab2:
            st.header("💼 Skills Analysis")
            
            skills = result['skills']
            if skills:
                st.subheader("🎯 Identified Skills")
                
                # Group skills by category
                tech_skills = [skill for skill in skills if skill.category == 'Technical']
                soft_skills = [skill for skill in skills if skill.category == 'Soft Skills']
                
                if tech_skills:
                    st.write("**Technical Skills:**")
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-tag">{skill.name}</span>', unsafe_allow_html=True)
                
                if soft_skills:
                    st.write("**Soft Skills:**")
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-tag">{skill.name}</span>', unsafe_allow_html=True)
            else:
                st.info("No skills detected in the resume.")
        
        with tab3:
            st.header("💡 Improvement Recommendations")
            
            recommendations = result['score'].recommendations
            
            if recommendations:
                for i, recommendation in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h3>{i}. {recommendation}</h3>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No specific recommendations at this time.")
        
        # Reset button
        if st.sidebar.button("🔄 Upload New Resume"):
            st.session_state.analysis_result = None
            st.rerun()
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>Welcome to VidyāMitra! 🎯</h2>
            <p>Your AI-powered career companion is ready to help you:</p>
            <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                <li>📊 Analyze your resume with AI</li>
                <li>💼 Identify your key skills and strengths</li>
                <li>🎯 Get personalized career recommendations</li>
                <li>📚 Discover skill gaps and learning resources</li>
                <li>💡 Receive actionable improvement tips</li>
            </ul>
            <p style="margin-top: 2rem;"><strong>Upload your resume to get started!</strong></p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
