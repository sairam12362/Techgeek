import streamlit as st
import os
import json
from typing import Dict, Any
from pathlib import Path
import tempfile

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
    
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.info("📝 Note: Full AI analysis requires OpenAI API key setup")
        
        # Display file info
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size} bytes")
        st.write(f"**File Type:** {uploaded_file.type}")
    
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
