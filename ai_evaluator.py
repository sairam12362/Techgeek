import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
from openai import OpenAI
from resume_parser import ResumeParser, Skill, WorkExperience, Education


@dataclass
class ResumeScore:
    overall_score: float
    sections: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


@dataclass
class SkillGap:
    skill_name: str
    current_level: str
    required_level: str
    importance: str
    learning_resources: List[str]


@dataclass
class CareerRecommendation:
    job_title: str
    match_score: float
    required_skills: List[str]
    missing_skills: List[str]
    salary_range: str
    growth_potential: str


class AIResumeEvaluator:
    def __init__(self, openai_api_key: str = None):
        self.client = OpenAI(api_key=openai_api_key or os.getenv('OPENAI_API_KEY'))
        self.parser = ResumeParser()
        
        # Enhanced career path data with more detailed requirements
        self.career_paths = {
            'Software Engineer': {
                'required_skills': ['python', 'javascript', 'git', 'sql', 'problem solving', 'data structures', 'algorithms', 'react', 'node.js'],
                'salary_range': '$70k - $150k',
                'growth_potential': 'High',
                'description': 'Design, develop and maintain software applications and systems'
            },
            'Data Scientist': {
                'required_skills': ['python', 'machine learning', 'data science', 'sql', 'statistics', 'tensorflow', 'pandas', 'numpy'],
                'salary_range': '$80k - $160k',
                'growth_potential': 'Very High',
                'description': 'Analyze complex data to help companies make better business decisions'
            },
            'Product Manager': {
                'required_skills': ['project management', 'communication', 'leadership', 'analytical', 'market research', 'strategy', 'agile'],
                'salary_range': '$75k - $140k',
                'growth_potential': 'High',
                'description': 'Lead product development and strategy from conception to launch'
            },
            'DevOps Engineer': {
                'required_skills': ['docker', 'kubernetes', 'aws', 'linux', 'automation', 'ci/cd', 'monitoring', 'security'],
                'salary_range': '$80k - $150k',
                'growth_potential': 'High',
                'description': 'Bridge development and operations to ensure smooth software deployment'
            },
            'Full Stack Developer': {
                'required_skills': ['react', 'node.js', 'python', 'sql', 'html', 'css', 'javascript', 'mongodb'],
                'salary_range': '$65k - $130k',
                'growth_potential': 'High',
                'description': 'Work on both front-end and back-end development of web applications'
            },
            'UX/UI Designer': {
                'required_skills': ['figma', 'adobe creative suite', 'user research', 'prototyping', 'wireframing', 'design thinking'],
                'salary_range': '$60k - $120k',
                'growth_potential': 'High',
                'description': 'Create user-centered designs for digital products and services'
            },
            'Cybersecurity Analyst': {
                'required_skills': ['network security', 'penetration testing', 'risk assessment', 'incident response', 'compliance'],
                'salary_range': '$70k - $140k',
                'growth_potential': 'Very High',
                'description': 'Protect organization systems and data from cyber threats'
            }
        }

    def evaluate_resume_structure(self, resume_data: Dict[str, Any]) -> ResumeScore:
        """Evaluate the structure and completeness of the resume"""
        scores = {}
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Contact information (20%)
        contact_score = 0
        if resume_data.get('contact_info', {}).get('email'):
            contact_score += 10
        if resume_data.get('contact_info', {}).get('phone'):
            contact_score += 10
        scores['contact_info'] = contact_score
        
        # Skills section (25%)
        skills = resume_data.get('skills', [])
        skills_score = min(len(skills) * 2, 25)
        scores['skills'] = skills_score
        
        # Work experience (30%)
        experience = resume_data.get('work_experience', [])
        experience_score = min(len(experience) * 10, 30)
        scores['work_experience'] = experience_score
        
        # Education (25%)
        education = resume_data.get('education', [])
        education_score = min(len(education) * 12, 25)
        scores['education'] = education_score
        
        overall_score = sum(scores.values())
        
        # Generate insights
        if contact_score == 20:
            strengths.append("Complete contact information provided")
        else:
            weaknesses.append("Missing or incomplete contact information")
            recommendations.append("Add email and phone number")
        
        if skills_score >= 20:
            strengths.append("Good variety of skills listed")
        else:
            weaknesses.append("Limited skills section")
            recommendations.append("Add more relevant skills")
        
        if experience_score >= 20:
            strengths.append("Solid work experience section")
        else:
            weaknesses.append("Limited work experience details")
            recommendations.append("Add more work experience with details")
        
        return ResumeScore(
            overall_score=overall_score,
            sections=scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )

    def analyze_skills_with_ai(self, resume_text: str, skills: List[Skill]) -> Dict[str, Any]:
        """Use AI to analyze and categorize skills more accurately"""
        try:
            prompt = f"""
            You are an expert career coach and technical recruiter. Analyze the following resume text and provide detailed skill analysis:
            
            Resume Text:
            {resume_text[:3000]}
            
            Current extracted skills: {[skill.name for skill in skills]}
            
            Please provide a comprehensive analysis in JSON format:
            {{
                "skill_proficiency": {{
                    "skill_name": {{"level": "Beginner|Intermediate|Advanced|Expert", "years_experience": number, "confidence": 0.0-1.0}}
                }},
                "skill_categories": {{
                    "technical": ["skill1", "skill2"],
                    "soft_skills": ["skill1", "skill2"],
                    "domain_specific": ["skill1", "skill2"]
                }},
                "missing_valuable_skills": ["skill1", "skill2"],
                "skill_trends": {{
                    "emerging_skills": ["skill1", "skill2"],
                    "in_demand_skills": ["skill1", "skill2"]
                }},
                "recommendations": ["specific recommendation 1", "specific recommendation 2"]
            }}
            
            Base your analysis on current industry trends and job market demands. Be specific and realistic.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert resume analyzer and career coach with deep knowledge of current industry trends and job market requirements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"AI analysis error: {e}")
            # Fallback to basic skill analysis
            return {
                "skill_proficiency": {
                    skill.name: {
                        "level": "Intermediate" if skill.experience_years and skill.experience_years > 2 else "Beginner",
                        "years_experience": skill.experience_years or 0,
                        "confidence": 0.7
                    } for skill in skills
                },
                "skill_categories": {
                    "technical": [skill.name for skill in skills if skill.category in ['Programming', 'Database', 'Web Development']],
                    "soft_skills": [skill.name for skill in skills if skill.category in ['Communication', 'Leadership', 'Project Management']],
                    "domain_specific": [skill.name for skill in skills if skill.category not in ['Programming', 'Database', 'Web Development', 'Communication', 'Leadership', 'Project Management']]
                },
                "missing_valuable_skills": ["Machine Learning", "Cloud Computing", "DevOps"],
                "skill_trends": {
                    "emerging_skills": ["AI/ML", "Blockchain"],
                    "in_demand_skills": ["Python", "JavaScript", "React", "AWS"]
                },
                "recommendations": ["Focus on cloud certifications", "Build portfolio projects"]
            }

    def identify_skill_gaps(self, current_skills: List[str], target_role: str) -> List[SkillGap]:
        """Identify skill gaps for a target career path"""
        if target_role not in self.career_paths:
            return []
        
        required_skills = self.career_paths[target_role]['required_skills']
        current_skill_names = [skill.lower() for skill in current_skills]
        
        gaps = []
        for skill in required_skills:
            if skill not in current_skill_names:
                gaps.append(SkillGap(
                    skill_name=skill,
                    current_level="Not Present",
                    required_level="Intermediate",
                    importance="High",
                    learning_resources=[
                        f"Online courses for {skill}",
                        f"Projects involving {skill}",
                        f"Certifications in {skill}"
                    ]
                ))
        
        return gaps

    def generate_career_recommendations(self, skills: List[Skill], experience: List[WorkExperience], resume_text: str = "") -> List[CareerRecommendation]:
        """Generate career recommendations based on skills, experience, and AI analysis"""
        current_skill_names = [skill.name.lower() for skill in skills]
        recommendations = []
        
        # Use AI to get personalized career recommendations
        try:
            ai_career_prompt = f"""
            Based on the following resume information, suggest the top 5 most suitable career paths:
            
            Skills: {[skill.name for skill in skills]}
            Experience: {len(experience)} positions
            Resume Summary: {resume_text[:1000]}
            
            Consider current job market trends, salary potential, and growth opportunities.
            For each career, provide:
            1. Job title
            2. Match percentage (0-100)
            3. Required skills
            4. Missing skills
            5. Realistic salary range
            6. Growth potential (Low/Medium/High)
            
            Return in JSON format with array of career objects.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career advisor with knowledge of current job market trends and salary data."},
                    {"role": "user", "content": ai_career_prompt}
                ],
                temperature=0.3
            )
            
            ai_result = json.loads(response.choices[0].message.content)
            
            # Convert AI result to CareerRecommendation objects
            for career_data in ai_result[:5]:
                rec = CareerRecommendation(
                    job_title=career_data.get('job_title', 'Software Engineer'),
                    match_score=career_data.get('match_percentage', 75),
                    required_skills=career_data.get('required_skills', []),
                    missing_skills=career_data.get('missing_skills', []),
                    salary_range=career_data.get('salary_range', '$70k - $120k'),
                    growth_potential=career_data.get('growth_potential', 'High')
                )
                recommendations.append(rec)
                
        except Exception as e:
            print(f"AI career recommendations error: {e}")
            # Fallback to traditional career matching
            for career_name, career_data in self.career_paths.items():
                required_skills = career_data['required_skills']
                matches = sum(1 for skill in required_skills if skill in current_skill_names)
                match_score = (matches / len(required_skills)) * 100 if required_skills else 0
                
                if match_score > 30:  # Only include careers with decent match
                    missing_skills = [skill for skill in required_skills if skill not in current_skill_names]
                    
                    rec = CareerRecommendation(
                        job_title=career_name,
                        match_score=match_score,
                        required_skills=required_skills,
                        missing_skills=missing_skills,
                        salary_range=career_data['salary_range'],
                        growth_potential=career_data['growth_potential']
                    )
                    recommendations.append(rec)
        
        # Sort by match score and return top 5
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:5]

    def generate_improvement_suggestions(self, resume_data: Dict[str, Any]) -> List[str]:
        """Generate specific improvement suggestions using AI"""
        prompt = f"""
        You are an expert career coach and resume writer. Analyze this resume and provide 8-10 specific, actionable improvement suggestions:
        
        Resume Data:
        {json.dumps(resume_data, indent=2, default=str)}
        
        Provide suggestions in these categories:
        1. Content improvements (specific phrases to add/remove)
        2. Formatting and structure suggestions
        3. Skills to highlight or acquire
        4. Experience presentation improvements
        5. Modern resume best practices
        6. ATS (Applicant Tracking System) optimization
        7. Quantifiable achievements to add
        8. Industry-specific recommendations
        
        Each suggestion should be:
- Specific and actionable
- Tailored to the experience level shown
- Based on current hiring trends
- Practical to implement

        Return as a JSON array of strings, each containing one complete suggestion.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career coach and professional resume writer with 15+ years of experience helping candidates land jobs at top companies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            suggestions = json.loads(response.choices[0].message.content)
            return suggestions if isinstance(suggestions, list) else ["Unable to generate suggestions at this time."]
        except Exception as e:
            print(f"AI suggestions error: {e}")
            return [
                "Add quantifiable achievements to your work experience",
                "Include a professional summary at the top of your resume",
                "Tailor your skills section to match job descriptions",
                "Use action verbs to start bullet points",
                "Ensure consistent formatting throughout"
            ]

    def complete_analysis(self, file_path: str) -> Dict[str, Any]:
        """Perform complete resume analysis"""
        # Parse resume
        resume_data = self.parser.parse_resume(file_path)
        
        # Evaluate structure
        score = self.evaluate_resume_structure(resume_data)
        
        # AI skill analysis
        skill_analysis = self.analyze_skills_with_ai(
            resume_data['raw_text'], 
            resume_data['skills']
        )
        
        # Generate career recommendations with AI
        skill_names = [skill.name for skill in resume_data['skills']]
        career_recommendations = self.generate_career_recommendations(
            resume_data['skills'], 
            resume_data['work_experience'],
            resume_data['raw_text']
        )
        
        # Generate improvement suggestions
        suggestions = self.generate_improvement_suggestions(resume_data)
        
        return {
            'resume_data': resume_data,
            'score': asdict(score),
            'skill_analysis': skill_analysis,
            'career_recommendations': [asdict(rec) for rec in career_recommendations],
            'improvement_suggestions': suggestions
        }


if __name__ == "__main__":
    # Test the evaluator
    evaluator = AIResumeEvaluator()
    
    # Example usage
    try:
        result = evaluator.complete_analysis("sample_resume.pdf")
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
