import streamlit as st
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib


class UserAuth:
    def __init__(self):
        self.users_file = "users.json"
        self.sessions_file = "sessions.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create necessary files if they don't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Load existing users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Check if user already exists
            if email in users:
                return {"success": False, "message": "User already exists"}
            
            # Add new user
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
            
            # Save users
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return {"success": True, "message": "User registered successfully"}
        
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user and create session"""
        try:
            # Load users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Check credentials
            if email not in users:
                return {"success": False, "message": "User not found"}
            
            if users[email]["password"] != self._hash_password(password):
                return {"success": False, "message": "Invalid password"}
            
            # Create session
            session_id = hashlib.sha256(f"{email}{datetime.now()}".encode()).hexdigest()
            session_data = {
                "email": email,
                "name": users[email]["name"],
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            # Load sessions
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            # Add new session
            sessions[session_id] = session_data
            
            # Save sessions
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
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate session and return user data"""
        try:
            # Load sessions
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            # Check if session exists
            if session_id not in sessions:
                return {"valid": False, "message": "Session not found"}
            
            session = sessions[session_id]
            
            # Check if session expired
            if datetime.fromisoformat(session["expires_at"]) < datetime.now():
                # Remove expired session
                del sessions[session_id]
                with open(self.sessions_file, 'w') as f:
                    json.dump(sessions, f, indent=2)
                return {"valid": False, "message": "Session expired"}
            
            # Load users to get updated profile
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            email = session["email"]
            return {
                "valid": True,
                "user": {
                    "email": email,
                    "name": users[email]["name"],
                    "profile": users[email]["profile"]
                }
            }
        
        except Exception as e:
            return {"valid": False, "message": f"Session validation failed: {str(e)}"}
    
    def logout_user(self, session_id: str) -> Dict[str, Any]:
        """Logout user by removing session"""
        try:
            # Load sessions
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            # Remove session
            if session_id in sessions:
                del sessions[session_id]
                
                # Save sessions
                with open(self.sessions_file, 'w') as f:
                    json.dump(sessions, f, indent=2)
                
                return {"success": True, "message": "Logout successful"}
            
            return {"success": False, "message": "Session not found"}
        
        except Exception as e:
            return {"success": False, "message": f"Logout failed: {str(e)}"}
    
    def update_profile(self, email: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            # Load users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Update profile
            if email in users:
                users[email]["profile"].update(profile_data)
                
                # Save users
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                
                return {"success": True, "message": "Profile updated successfully"}
            
            return {"success": False, "message": "User not found"}
        
        except Exception as e:
            return {"success": False, "message": f"Profile update failed: {str(e)}"}
    
    def save_resume_analysis(self, email: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save resume analysis to user profile"""
        try:
            # Load users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Add analysis to user profile
            if email in users:
                analysis_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "score": analysis_data.get("score", {}),
                    "skills": analysis_data.get("resume_data", {}).get("skills", []),
                    "career_recommendations": analysis_data.get("career_recommendations", [])
                }
                
                users[email]["profile"]["resume_analyses"].append(analysis_entry)
                
                # Keep only last 10 analyses
                if len(users[email]["profile"]["resume_analyses"]) > 10:
                    users[email]["profile"]["resume_analyses"] = users[email]["profile"]["resume_analyses"][-10:]
                
                # Save users
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                
                return {"success": True, "message": "Analysis saved successfully"}
            
            return {"success": False, "message": "User not found"}
        
        except Exception as e:
            return {"success": False, "message": f"Failed to save analysis: {str(e)}"}


def show_login_page():
    """Display login page"""
    # Apply the same modern CSS styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
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
        
        .login-header {
            font-size: 4rem;
            font-weight: 900;
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);
            animation: glow 2s ease-in-out infinite alternate;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5); }
            to { text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 70px rgba(255, 255, 255, 0.6); }
        }
        
        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
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
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="login-header" style="color: white; text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);">🎯 VidyāMitra</h1>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container"><p style="text-align: center; color: white; font-size: 1.1rem; margin: 0;">🔐 Login to your AI Career Agent</p></div>', unsafe_allow_html=True)
    
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
    
    # Register link
    if st.button("Don't have an account? Register"):
        st.session_state.show_register = True
        st.rerun()


def show_register_page():
    """Display registration page"""
    # Apply the same modern CSS styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
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
        
        .register-header {
            font-size: 4rem;
            font-weight: 900;
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);
            animation: glow 2s ease-in-out infinite alternate;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5); }
            to { text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 70px rgba(255, 255, 255, 0.6); }
        }
        
        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
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
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="register-header" style="color: white; text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);">🎯 VidyāMitra</h1>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container"><p style="text-align: center; color: white; font-size: 1.1rem; margin: 0;">📝 Create your AI Career Agent account</p></div>', unsafe_allow_html=True)
    
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
    
    # Login link
    if st.button("Already have an account? Login"):
        st.session_state.show_register = False
        st.rerun()


def show_profile_page():
    """Display user profile page"""
    if 'user' not in st.session_state:
        st.error("Please login to view your profile")
        return
    
    # Apply modern CSS styling to profile page
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
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
        
        .profile-header {
            font-size: 3.5rem;
            font-weight: 900;
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);
            animation: glow 2s ease-in-out infinite alternate;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5); }
            to { text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 70px rgba(255, 255, 255, 0.6); }
        }
        
        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
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
    """, unsafe_allow_html=True)
    
    user = st.session_state.user
    st.markdown('<h1 class="profile-header" style="color: white; text-shadow: 0 0 50px rgba(255, 255, 255, 0.8), 0 0 100px rgba(255, 255, 255, 0.6);">🎯 VidyāMitra</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="glass-container"><p style="text-align: center; color: white; font-size: 1.2rem; margin: 0;">👤 {user["name"]}\'s Profile</p></div>', unsafe_allow_html=True)
    
    # Profile information
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
                auth = UserAuth()
                profile_data = {
                    "skills": [skill.strip() for skill in skills.split(',') if skill.strip()],
                    "experience": experience,
                    "career_goals": career_goals
                }
                
                result = auth.update_profile(user['email'], profile_data)
                
                if result["success"]:
                    st.success(result["message"])
                    # Update session state
                    st.session_state.user['profile'].update(profile_data)
                    st.rerun()
                else:
                    st.error(result["message"])
    
    with col2:
        st.subheader("📊 Statistics")
        
        # Resume analyses
        analyses = user['profile'].get('resume_analyses', [])
        st.metric("Resume Analyses", len(analyses))
        
        if analyses:
            latest_score = analyses[-1].get('score', {}).get('overall_score', 0)
            st.metric("Latest Score", f"{latest_score}/100")
        
        # Skills count
        skills_count = len(user['profile'].get('skills', []))
        st.metric("Skills Listed", skills_count)
    
    # Resume history
    if analyses:
        st.subheader("📈 Resume Analysis History")
        
        for i, analysis in enumerate(reversed(analyses[-5:])):  # Show last 5
            with st.expander(f"Analysis from {analysis['timestamp'][:10]}"):
                score = analysis.get('score', {}).get('overall_score', 0)
                st.write(f"**Score:** {score}/100")
                
                skills = analysis.get('skills', [])
                if skills:
                    st.write(f"**Skills:** {', '.join([skill.get('name', 'Unknown') for skill in skills[:5]])}")
                
                recommendations = analysis.get('career_recommendations', [])
                if recommendations:
                    top_rec = recommendations[0].get('job_title', 'Unknown')
                    st.write(f"**Top Recommendation:** {top_rec}")
    
    # Logout button
    if st.button("🚪 Logout"):
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


def check_authentication():
    """Check if user is authenticated"""
    if 'session_id' in st.session_state:
        auth = UserAuth()
        result = auth.validate_session(st.session_state.session_id)
        
        if result["valid"]:
            st.session_state.user = result["user"]
            return True
        else:
            # Clear invalid session
            if 'session_id' in st.session_state:
                del st.session_state.session_id
            if 'user' in st.session_state:
                del st.session_state.user
            return False
    
    return False


if __name__ == "__main__":
    # Test authentication
    auth = UserAuth()
    
    # Test registration
    result = auth.register_user("test@example.com", "password123", "Test User")
    print(f"Registration: {result}")
    
    # Test login
    result = auth.login_user("test@example.com", "password123")
    print(f"Login: {result}")
    
    if result["success"]:
        # Test session validation
        session_result = auth.validate_session(result["session_id"])
        print(f"Session validation: {session_result}")
