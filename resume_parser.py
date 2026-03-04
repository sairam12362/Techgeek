import os
import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import PyPDF2
from docx import Document
import pandas as pd
from dataclasses import dataclass


@dataclass
class ResumeSection:
    title: str
    content: str
    keywords: List[str]


@dataclass
class Skill:
    name: str
    category: str
    proficiency: str
    experience_years: Optional[float] = None


@dataclass
class WorkExperience:
    company: str
    position: str
    duration: str
    description: str


@dataclass
class Education:
    institution: str
    degree: str
    year: str
    gpa: Optional[str] = None


class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        # Common skill keywords
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
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text

    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")

    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract email and phone from resume text"""
        email = re.search(self.email_pattern, text)
        phone = re.search(self.phone_pattern, text)
        
        return {
            'email': email.group() if email else '',
            'phone': phone.group() if phone else ''
        }

    def extract_skills(self, text: str) -> List[Skill]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        skills = []
        
        # Extract technical skills
        for skill in self.tech_skills:
            if skill in text_lower:
                skills.append(Skill(
                    name=skill,
                    category='Technical',
                    proficiency='Intermediate'  # Default, will be refined by AI
                ))
        
        # Extract soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                skills.append(Skill(
                    name=skill,
                    category='Soft Skills',
                    proficiency='Intermediate'
                ))
        
        return skills

    def extract_work_experience(self, text: str) -> List[WorkExperience]:
        """Extract work experience from resume text"""
        experiences = []
        
        # Simple pattern matching for work experience
        # This is a basic implementation - can be enhanced with NLP
        lines = text.split('\n')
        current_exp = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Look for patterns that suggest work experience
            if any(keyword in line.lower() for keyword in ['experience', 'work', 'employment']):
                # Look for the next few lines for company/position info
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and len(next_line) > 10:
                        # Simple heuristic - if line contains years, it might be duration
                        if re.search(r'\b(19|20)\d{2}\b', next_line):
                            duration = next_line
                            company_pos = line
                            experiences.append(WorkExperience(
                                company=company_pos.split(' at ')[-1] if ' at ' in company_pos else company_pos,
                                position=company_pos.split(' at ')[0] if ' at ' in company_pos else company_pos,
                                duration=duration,
                                description=""
                            ))
                        break
        
        return experiences

    def extract_education(self, text: str) -> List[Education]:
        """Extract education information from resume text"""
        education = []
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if any(keyword in line for keyword in ['university', 'college', 'bachelor', 'master', 'phd', 'degree']):
                # Look for degree information in surrounding lines
                for j in range(max(0, i-1), min(i+3, len(lines))):
                    context_line = lines[j].strip()
                    if context_line and len(context_line) > 10:
                        # Extract year if present
                        year_match = re.search(r'\b(19|20)\d{2}\b', context_line)
                        year = year_match.group() if year_match else ''
                        
                        education.append(Education(
                            institution=context_line,
                            degree=line.title(),
                            year=year
                        ))
                        break
        
        return education

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Main method to parse resume and extract all information"""
        file_extension = Path(file_path).suffix.lower()
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT files.")
        
        # Extract all information
        parsed_data = {
            'raw_text': text,
            'contact_info': self.extract_contact_info(text),
            'skills': self.extract_skills(text),
            'work_experience': self.extract_work_experience(text),
            'education': self.extract_education(text),
            'file_type': file_extension
        }
        
        return parsed_data


if __name__ == "__main__":
    # Test the parser
    parser = ResumeParser()
    
    # Example usage
    try:
        result = parser.parse_resume("sample_resume.pdf")
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
