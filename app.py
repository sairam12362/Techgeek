import streamlit as st
import os
import json
from typing import Dict, Any
from pathlib import Path
import tempfile
from ai_evaluator import AIResumeEvaluator
from resume_parser import ResumeParser
from auth import UserAuth, check_authentication, show_login_page, show_register_page, show_profile_page
from export_manager import show_export_page
from training_resources import TrainingResourceManager


def main():
    st.set_page_config(
        page_title="VidyāMitra - AI Career Agent",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS - Modern Cutting Edge Design
    st.markdown("""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Animated gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Glass morphism containers */
        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .glass-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        /* Main header with glow effect */
        .main-header {
            font-size: 4rem;
            font-weight: 900;
            color: white !important;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);
            animation: glow 2s ease-in-out infinite alternate;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5); }
            to { text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 70px rgba(255, 255, 255, 0.6); }
        }
        
        /* Interactive metric cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            margin: 1rem 0;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.5s;
            opacity: 0;
        }
        
        .metric-card:hover::before {
            animation: shimmer 0.5s ease;
            opacity: 1;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .metric-card:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        
        .metric-value {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            animation: countUp 2s ease-out;
        }
        
        @keyframes countUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Interactive skill tags */
        .skill-tag {
            display: inline-block;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.1));
            backdrop-filter: blur(10px);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            margin: 0.5rem;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .skill-tag::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: all 0.5s ease;
        }
        
        .skill-tag:hover::before {
            width: 100%;
            height: 100%;
        }
        
        .skill-tag:hover {
            transform: translateY(-3px) scale(1.1);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            color: #fff;
        }
        
        /* Modern recommendation cards */
        .recommendation-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: 1rem 0;
            transition: all 0.4s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .recommendation-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .recommendation-card:hover::before {
            left: 100%;
        }
        
        .recommendation-card:hover {
            transform: translateX(10px) scale(1.02);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }
        
        /* Gap cards with warning animation */
        .gap-card {
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(255, 152, 0, 0.1));
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 193, 7, 0.3);
            margin: 1rem 0;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .gap-card::before {
            content: '⚠️';
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.5rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .gap-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 193, 7, 0.2);
        }
        
        /* Interactive tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
            color: white;
        }
        
        /* Animated progress bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            background-size: 200% 100%;
            animation: progressAnimation 2s ease-in-out;
        }
        
        @keyframes progressAnimation {
            0% { background-position: 0% 0%; }
            100% { background-position: 200% 0%; }
        }
        
        /* Floating particles background */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            animation: float 6s infinite ease-in-out;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            33% { transform: translateY(-30px) translateX(20px); }
            66% { transform: translateY(20px) translateX(-20px); }
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2));
        }
    </style>
    
    <!-- Floating particles -->
    <div class="particles">
        <div class="particle" style="left: 10%; top: 20%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; top: 80%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 30%; top: 40%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 40%; top: 60%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 50%; top: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 60%; top: 70%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; top: 50%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 80%; top: 25%; animation-delay: 7s;"></div>
        <div class="particle" style="left: 90%; top: 75%; animation-delay: 8s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        # Show login or register page
        if st.session_state.get('show_register', False):
            show_register_page()
        else:
            show_login_page()
        return
    
    # User is authenticated
    user = st.session_state.user
    
    # Sidebar with navigation
    st.sidebar.title(f"👤 {user['name']}")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate",
        ["🏠 Dashboard", "👤 Profile", "📤 Export & Share", "🚪 Logout"]
    )
    
    if page == "🚪 Logout":
        auth = UserAuth()
        result = auth.logout_user(st.session_state.session_id)
        
        if result["success"]:
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success(result["message"])
            st.rerun()
        else:
            st.error(result["message"])
        return
    
    if page == "👤 Profile":
        show_profile_page()
        return
    
    if page == "📤 Export & Share":
        if 'analysis_result' in st.session_state:
            show_export_page(st.session_state.analysis_result, user)
        else:
            st.warning("Please analyze a resume first to access export features.")
        return
    
    # Main dashboard with glass morphism
    st.markdown('<h1 class="main-header" style="color: white !important; text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6); filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));">🎯 VidyāMitra</h1>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container"><p style="text-align: center; color: white; font-size: 1.2rem; font-weight: 500; margin: 0;">AI-Powered Resume Evaluator, Trainer & Career Planner</p></div>', unsafe_allow_html=True)
    
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
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    
    # Process uploaded file
    if uploaded_file and not st.session_state.file_processed:
        with st.spinner("🔍 Analyzing your resume..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Initialize evaluator
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
                    return
                
                evaluator = AIResumeEvaluator(api_key)
                
                # Perform analysis
                result = evaluator.complete_analysis(tmp_file_path)
                st.session_state.analysis_result = result
                st.session_state.file_processed = True
                
                # Save analysis to user profile
                auth = UserAuth()
                auth.save_resume_analysis(user['email'], result)
                
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
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Overview", 
            "💼 Skills Analysis", 
            "🎯 Career Recommendations", 
            "📚 Skill Gaps", 
            "💡 Improvement Tips",
            "📖 Training Resources"
        ])
        
        with tab1:
            st.header("📈 Resume Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score = result['score']['overall_score']
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{score}/100</div>
                    <div>Overall Score</div>
                </div>
                ''', unsafe_allow_html=True)
        
            with col2:
                skills_count = len(result['resume_data']['skills'])
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{skills_count}</div>
                    <div>Skills Identified</div>
                </div>
                ''', unsafe_allow_html=True)
        
            with col3:
                exp_count = len(result['resume_data']['work_experience'])
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{exp_count}</div>
                    <div>Work Experience</div>
                </div>
                ''', unsafe_allow_html=True)
        
            with col4:
                edu_count = len(result['resume_data']['education'])
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{edu_count}</div>
                    <div>Education</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Score breakdown
            st.subheader("📊 Score Breakdown")
            sections = result['score']['sections']
            
            for section, score in sections.items():
                st.write(f"**{section.replace('_', ' ').title()}:** {score}/100")
                st.progress(score / 100)
            
            # Strengths and Weaknesses
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Strengths")
                for strength in result['score']['strengths']:
                    st.write(f"• {strength}")
            
            with col2:
                st.subheader("⚠️ Areas for Improvement")
                for weakness in result['score']['weaknesses']:
                    st.write(f"• {weakness}")
        
        with tab2:
            st.header("💼 Skills Analysis")
            
            # Skills display
            skills = result['resume_data']['skills']
            if skills:
                st.subheader("🎯 Identified Skills")
                
                # Group skills by category
                tech_skills = [skill for skill in skills if skill.get('category', '').lower() == 'technical']
                soft_skills = [skill for skill in skills if skill.get('category', '').lower() == 'soft skills']
                
                if tech_skills:
                    st.write("**Technical Skills:**")
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-tag">{skill["name"]}</span>', unsafe_allow_html=True)
                
                if soft_skills:
                    st.write("**Soft Skills:**")
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-tag">{skill["name"]}</span>', unsafe_allow_html=True)
            
            # AI Analysis
            if 'skill_analysis' in result and 'error' not in result['skill_analysis']:
                st.subheader("🤖 AI-Powered Insights")
                st.json(result['skill_analysis'])
        
        with tab3:
            st.header("🎯 Career Recommendations")
            
            recommendations = result['career_recommendations']
            
            if recommendations:
                for rec in recommendations[:5]:  # Show top 5
                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h3>{rec['job_title']}</h3>
                            <p><strong>Match Score:</strong> {rec['match_score']:.1f}%</p>
                            <p><strong>Salary Range:</strong> {rec['salary_range']}</p>
                            <p><strong>Growth Potential:</strong> {rec['growth_potential']}</p>
                            <p><strong>Required Skills:</strong> {', '.join(rec['required_skills'])}</p>
                            {f"<p><strong>Missing Skills:</strong> {', '.join(rec['missing_skills'])}</p>" if rec['missing_skills'] else ""}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No career recommendations available yet.")
        
        with tab4:
            st.header("📚 Skill Gap Analysis")
            
            # Generate skill gaps for top recommended career
            if recommendations:
                top_career = recommendations[0]['job_title']
                st.subheader(f"Skill Gaps for {top_career}")
                
                current_skills = [skill['name'] for skill in result['resume_data']['skills']]
                
                # Simple skill gap analysis
                required_skills = recommendations[0]['required_skills']
                missing_skills = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in current_skills]]
                
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"""
                        <div class="gap-card">
                            <h4 style="color: white; margin-top: 0;">🔧 {skill}</h4>
                            <p style="color: rgba(255,255,255,0.9);"><strong>Importance:</strong> High</p>
                            <p style="color: rgba(255,255,255,0.9);"><strong>Recommended Learning:</strong></p>
                            <ul style="color: rgba(255,255,255,0.8);">
                                <li>Online courses and tutorials</li>
                                <li>Hands-on projects</li>
                                <li>Certification programs</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("🎉 No skill gaps identified for your top career recommendation!")
            else:
                st.info("Upload a resume to see skill gap analysis.")
        
        with tab5:
            st.header("💡 Improvement Suggestions")
            
            suggestions = result['improvement_suggestions']
            
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
            else:
                st.info("No improvement suggestions available.")
        
        with tab6:
            st.header("📖 Training Resources")
            
            # Initialize training resource manager
            training_manager = TrainingResourceManager()
            
            # Get top career recommendation
            if recommendations:
                top_career = recommendations[0]['job_title']
                st.subheader(f"Resources for {top_career}")
                
                # Get career-specific resources
                career_resources = training_manager.get_career_specific_resources(top_career)
                
                if career_resources:
                    for resource in career_resources:
                        with st.expander(f"📚 {resource.title}"):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**Provider:** {resource.provider}")
                                st.write(f"**Type:** {resource.type}")
                                st.write(f"**Duration:** {resource.duration}")
                                st.write(f"**Difficulty:** {resource.difficulty}")
                                st.write(f"**Rating:** ⭐ {resource.rating}/5")
                                st.write(f"**Cost:** {resource.cost}")
                                st.write(f"**Skills Covered:** {', '.join(resource.skills_covered)}")
                            
                            with col2:
                                if resource.url != "N/A":
                                    st.markdown(f"[🔗 Visit]({resource.url})")
                else:
                    st.info("No specific resources found for this career path.")
            else:
                st.info("Analyze a resume to get personalized training resources.")
        
        # Reset button
        if st.sidebar.button("🔄 Upload New Resume"):
            st.session_state.file_processed = False
            st.session_state.analysis_result = None
            st.rerun()
    
    else:
        # Welcome message with glass morphism
        st.markdown("""
        <div class="glass-container" style="text-align: center;">
            <h2 style="color: white; margin-bottom: 1rem;">Welcome back to VidyāMitra! 🎯</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 2rem;">Your AI-powered career companion is ready to help you:</p>
            <ul style="text-align: left; max-width: 600px; margin: 0 auto; color: rgba(255,255,255,0.8); line-height: 1.8;">
                <li>📊 Analyze your resume with AI</li>
                <li>💼 Identify your key skills and strengths</li>
                <li>🎯 Get personalized career recommendations</li>
                <li>📚 Discover skill gaps and learning resources</li>
                <li>💡 Receive actionable improvement tips</li>
            </ul>
            <p style="margin-top: 2rem; color: white; font-weight: 600;"><strong>Upload your resume to get started!</strong></p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
