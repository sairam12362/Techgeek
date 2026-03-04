import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import base64
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


class ExportManager:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for PDF export"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f77b4')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        ))
    
    def generate_pdf_report(self, analysis_data: Dict[str, Any], user_info: Dict[str, Any] = None) -> BytesIO:
        """Generate PDF report of resume analysis"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72)
        story = []
        
        # Title
        title = Paragraph("VidyāMitra Resume Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # User information
        if user_info:
            user_text = f"Name: {user_info.get('name', 'N/A')}<br/>Email: {user_info.get('email', 'N/A')}"
            story.append(Paragraph(user_text, self.styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Date
        date_text = f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(date_text, self.styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Overall Score
        score_data = analysis_data.get('score', {})
        overall_score = score_data.get('overall_score', 0)
        
        story.append(Paragraph("Overall Resume Score", self.styles['CustomHeading']))
        score_text = f"Your resume scored <b>{overall_score}/100</b>"
        story.append(Paragraph(score_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Score Breakdown
        if 'sections' in score_data:
            story.append(Paragraph("Score Breakdown", self.styles['CustomHeading']))
            
            section_data = []
            section_data.append(['Section', 'Score'])
            
            for section, score in score_data['sections'].items():
                section_name = section.replace('_', ' ').title()
                section_data.append([section_name, f"{score}/100"])
            
            table = Table(section_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Strengths
        if 'strengths' in score_data and score_data['strengths']:
            story.append(Paragraph("Strengths", self.styles['CustomHeading']))
            for strength in score_data['strengths']:
                story.append(Paragraph(f"• {strength}", self.styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Areas for Improvement
        if 'weaknesses' in score_data and score_data['weaknesses']:
            story.append(Paragraph("Areas for Improvement", self.styles['CustomHeading']))
            for weakness in score_data['weaknesses']:
                story.append(Paragraph(f"• {weakness}", self.styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Skills Analysis
        resume_data = analysis_data.get('resume_data', {})
        skills = resume_data.get('skills', [])
        
        if skills:
            story.append(Paragraph("Identified Skills", self.styles['CustomHeading']))
            
            # Group skills by category
            tech_skills = [skill for skill in skills if skill.get('category', '').lower() == 'technical']
            soft_skills = [skill for skill in skills if skill.get('category', '').lower() == 'soft skills']
            
            if tech_skills:
                story.append(Paragraph("Technical Skills:", self.styles['Heading3']))
                for skill in tech_skills:
                    story.append(Paragraph(f"• {skill.get('name', 'Unknown')}", self.styles['Normal']))
                story.append(Spacer(1, 10))
            
            if soft_skills:
                story.append(Paragraph("Soft Skills:", self.styles['Heading3']))
                for skill in soft_skills:
                    story.append(Paragraph(f"• {skill.get('name', 'Unknown')}", self.styles['Normal']))
                story.append(Spacer(1, 20))
        
        # Career Recommendations
        recommendations = analysis_data.get('career_recommendations', [])
        if recommendations:
            story.append(Paragraph("Career Recommendations", self.styles['CustomHeading']))
            
            for i, rec in enumerate(recommendations[:3], 1):  # Top 3
                story.append(Paragraph(f"{i}. {rec.get('job_title', 'Unknown')}", self.styles['Heading3']))
                story.append(Paragraph(f"   Match Score: {rec.get('match_score', 0):.1f}%", self.styles['Normal']))
                story.append(Paragraph(f"   Salary Range: {rec.get('salary_range', 'N/A')}", self.styles['Normal']))
                story.append(Paragraph(f"   Growth Potential: {rec.get('growth_potential', 'N/A')}", self.styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_csv_export(self, analysis_data: Dict[str, Any]) -> BytesIO:
        """Generate CSV export of analysis data"""
        buffer = BytesIO()
        
        # Prepare data for CSV
        csv_data = []
        
        # Basic information
        csv_data.append(['Metric', 'Value'])
        csv_data.append(['Analysis Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        csv_data.append(['Overall Score', analysis_data.get('score', {}).get('overall_score', 0)])
        csv_data.append([])
        
        # Score breakdown
        sections = analysis_data.get('score', {}).get('sections', {})
        csv_data.append(['Section', 'Score'])
        for section, score in sections.items():
            csv_data.append([section.replace('_', ' ').title(), score])
        csv_data.append([])
        
        # Skills
        skills = analysis_data.get('resume_data', {}).get('skills', [])
        if skills:
            csv_data.append(['Skill Name', 'Category', 'Proficiency'])
            for skill in skills:
                csv_data.append([
                    skill.get('name', 'Unknown'),
                    skill.get('category', 'Unknown'),
                    skill.get('proficiency', 'Unknown')
                ])
            csv_data.append([])
        
        # Career recommendations
        recommendations = analysis_data.get('career_recommendations', [])
        if recommendations:
            csv_data.append(['Job Title', 'Match Score', 'Salary Range', 'Growth Potential'])
            for rec in recommendations:
                csv_data.append([
                    rec.get('job_title', 'Unknown'),
                    rec.get('match_score', 0),
                    rec.get('salary_range', 'N/A'),
                    rec.get('growth_potential', 'N/A')
                ])
        
        # Write to CSV
        df = pd.DataFrame(csv_data)
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        return buffer
    
    def generate_json_export(self, analysis_data: Dict[str, Any]) -> str:
        """Generate JSON export of analysis data"""
        export_data = {
            'export_date': datetime.now().isoformat(),
            'analysis_data': analysis_data
        }
        return json.dumps(export_data, indent=2, default=str)
    
    def create_shareable_link(self, analysis_data: Dict[str, Any]) -> str:
        """Create a shareable link (mock implementation)"""
        # In a real implementation, this would create a unique URL
        # For now, return a mock link
        analysis_id = hash(str(analysis_data))
        return f"https://vidyamitra.app/shared/{abs(analysis_id) % 1000000}"


def show_export_page(analysis_data: Dict[str, Any], user_info: Dict[str, Any] = None):
    """Display export options"""
    st.title("📤 Export & Share Analysis")
    
    export_manager = ExportManager()
    
    # Export options
    st.subheader("📄 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF Report", type="primary"):
            try:
                pdf_buffer = export_manager.generate_pdf_report(analysis_data, user_info)
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"vidyamitra_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        if st.button("📊 Download CSV"):
            try:
                csv_buffer = export_manager.generate_csv_export(analysis_data)
                st.download_button(
                    label="Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"vidyamitra_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error generating CSV: {str(e)}")
    
    with col3:
        if st.button("📋 Download JSON"):
            try:
                json_data = export_manager.generate_json_export(analysis_data)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"vidyamitra_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error generating JSON: {str(e)}")
    
    st.divider()
    
    # Share options
    st.subheader("🔗 Share Options")
    
    # Generate shareable link
    shareable_link = export_manager.create_shareable_link(analysis_data)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.text_input("Shareable Link", value=shareable_link, disabled=True)
    
    with col2:
        if st.button("📋 Copy Link"):
            st.write("Link copied to clipboard!")
    
    # Email sharing (mock)
    st.subheader("📧 Email Analysis")
    
    with st.form("email_form"):
        recipient_email = st.text_input("Recipient Email", placeholder="Enter email address")
        message = st.text_area("Personal Message (Optional)", placeholder="Add a personal message...")
        send_button = st.form_submit_button("📤 Send Email")
        
        if send_button and recipient_email:
            # In a real implementation, this would send an actual email
            st.success(f"Analysis sent to {recipient_email}!")
    
    # Social sharing
    st.subheader("🌐 Share on Social Media")
    
    # Prepare share text
    score = analysis_data.get('score', {}).get('overall_score', 0)
    share_text = f"I just analyzed my resume with VidyāMitra and scored {score}/100! 🎯"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📘 Share on LinkedIn"):
            st.info("Opening LinkedIn share dialog...")
    
    with col2:
        if st.button("🐦 Share on Twitter"):
            st.info("Opening Twitter share dialog...")
    
    with col3:
        if st.button("📱 Share on WhatsApp"):
            st.info("Opening WhatsApp share dialog...")
    
    # Preview
    st.divider()
    st.subheader("👁️ Preview")
    
    # Show a preview of the analysis
    with st.expander("📊 Analysis Summary Preview"):
        st.write(f"**Overall Score:** {score}/100")
        
        # Top skills
        skills = analysis_data.get('resume_data', {}).get('skills', [])
        if skills:
            st.write("**Top Skills:**")
            for skill in skills[:5]:
                st.write(f"• {skill.get('name', 'Unknown')}")
        
        # Top recommendation
        recommendations = analysis_data.get('career_recommendations', [])
        if recommendations:
            top_rec = recommendations[0]
            st.write(f"**Top Career Recommendation:** {top_rec.get('job_title', 'Unknown')}")
            st.write(f"**Match Score:** {top_rec.get('match_score', 0):.1f}%")


if __name__ == "__main__":
    # Test export functionality
    from ai_evaluator import AIResumeEvaluator
    
    # Sample data for testing
    sample_analysis = {
        'score': {
            'overall_score': 85,
            'sections': {
                'contact_info': 20,
                'skills': 22,
                'work_experience': 25,
                'education': 18
            },
            'strengths': ['Good skills variety', 'Solid experience'],
            'weaknesses': ['Missing certifications'],
            'recommendations': ['Add more projects']
        },
        'resume_data': {
            'skills': [
                {'name': 'Python', 'category': 'Technical', 'proficiency': 'Advanced'},
                {'name': 'JavaScript', 'category': 'Technical', 'proficiency': 'Intermediate'},
                {'name': 'Leadership', 'category': 'Soft Skills', 'proficiency': 'Advanced'}
            ]
        },
        'career_recommendations': [
            {
                'job_title': 'Software Engineer',
                'match_score': 92.5,
                'salary_range': '$80k - $120k',
                'growth_potential': 'High'
            }
        ]
    }
    
    sample_user = {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    # Test PDF generation
    export_manager = ExportManager()
    pdf_buffer = export_manager.generate_pdf_report(sample_analysis, sample_user)
    print(f"PDF generated successfully. Size: {len(pdf_buffer.getvalue())} bytes")
    
    # Test JSON export
    json_data = export_manager.generate_json_export(sample_analysis)
    print(f"JSON export generated. Length: {len(json_data)} characters")
