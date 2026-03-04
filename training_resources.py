from typing import Dict, List, Any
from dataclasses import dataclass
import json


@dataclass
class TrainingResource:
    title: str
    provider: str
    type: str  # 'course', 'tutorial', 'certification', 'book', 'video'
    duration: str
    difficulty: str  # 'Beginner', 'Intermediate', 'Advanced'
    url: str
    rating: float
    cost: str
    skills_covered: List[str]


@dataclass
class LearningPath:
    skill_name: str
    current_level: str
    target_level: str
    estimated_duration: str
    resources: List[TrainingResource]
    milestones: List[str]


class TrainingResourceManager:
    def __init__(self):
        self.resources_db = self._initialize_resources()
    
    def _initialize_resources(self) -> Dict[str, List[TrainingResource]]:
        """Initialize training resources database"""
        resources = {
            'python': [
                TrainingResource(
                    title="Python for Everybody",
                    provider="Coursera",
                    type="course",
                    duration="8 weeks",
                    difficulty="Beginner",
                    url="https://www.coursera.org/specializations/python",
                    rating=4.8,
                    cost="Free (with certificate)",
                    skills_covered=["python", "programming", "data structures"]
                ),
                TrainingResource(
                    title="Complete Python Bootcamp",
                    provider="Udemy",
                    type="course",
                    duration="22 hours",
                    difficulty="Beginner",
                    url="https://www.udemy.com/course/complete-python-bootcamp/",
                    rating=4.6,
                    cost="$19.99",
                    skills_covered=["python", "web development", "data science"]
                ),
                TrainingResource(
                    title="Python Crash Course Book",
                    provider="O'Reilly",
                    type="book",
                    duration="Self-paced",
                    difficulty="Beginner",
                    url="https://nostarch.com/pythoncrashcourse2e",
                    rating=4.7,
                    cost="$39.99",
                    skills_covered=["python", "programming", "projects"]
                )
            ],
            'javascript': [
                TrainingResource(
                    title="JavaScript: The Complete Guide",
                    provider="Udemy",
                    type="course",
                    duration="27 hours",
                    difficulty="Beginner",
                    url="https://www.udemy.com/course/javascript-the-complete-guide/",
                    rating=4.7,
                    cost="$19.99",
                    skills_covered=["javascript", "web development", "es6"]
                ),
                TrainingResource(
                    title="freeCodeCamp JavaScript",
                    provider="freeCodeCamp",
                    type="tutorial",
                    duration="300 hours",
                    difficulty="Beginner",
                    url="https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                    rating=4.8,
                    cost="Free",
                    skills_covered=["javascript", "algorithms", "data structures"]
                )
            ],
            'react': [
                TrainingResource(
                    title="Modern React with Redux",
                    provider="Udemy",
                    type="course",
                    duration="48 hours",
                    difficulty="Intermediate",
                    url="https://www.udemy.com/course/react-redux/",
                    rating=4.7,
                    cost="$19.99",
                    skills_covered=["react", "redux", "javascript"]
                ),
                TrainingResource(
                    title="React Documentation",
                    provider="React",
                    type="tutorial",
                    duration="Self-paced",
                    difficulty="Beginner",
                    url="https://react.dev/",
                    rating=4.9,
                    cost="Free",
                    skills_covered=["react", "hooks", "components"]
                )
            ],
            'machine learning': [
                TrainingResource(
                    title="Machine Learning Specialization",
                    provider="Coursera",
                    type="course",
                    duration="3 months",
                    difficulty="Intermediate",
                    url="https://www.coursera.org/specializations/machine-learning-introduction",
                    rating=4.8,
                    cost="Free (with certificate)",
                    skills_covered=["machine learning", "python", "algorithms"]
                ),
                TrainingResource(
                    title="Hands-On Machine Learning Book",
                    provider="O'Reilly",
                    type="book",
                    duration="Self-paced",
                    difficulty="Intermediate",
                    url="https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/",
                    rating=4.7,
                    cost="$54.99",
                    skills_covered=["machine learning", "tensorflow", "scikit-learn"]
                )
            ],
            'aws': [
                TrainingResource(
                    title="AWS Certified Solutions Architect",
                    provider="Udemy",
                    type="course",
                    duration="22 hours",
                    difficulty="Intermediate",
                    url="https://www.udemy.com/course/aws-certified-solutions-architect-associate/",
                    rating=4.7,
                    cost="$19.99",
                    skills_covered=["aws", "cloud computing", "architecture"]
                ),
                TrainingResource(
                    title="AWS Training and Certification",
                    provider="Amazon",
                    type="certification",
                    duration="Varies",
                    difficulty="Beginner",
                    url="https://aws.amazon.com/training/",
                    rating=4.6,
                    cost="Varies",
                    skills_covered=["aws", "cloud", "services"]
                )
            ],
            'docker': [
                TrainingResource(
                    title="Docker Mastery",
                    provider="Udemy",
                    type="course",
                    duration="15 hours",
                    difficulty="Intermediate",
                    url="https://www.udemy.com/course/docker-mastery/",
                    rating=4.7,
                    cost="$19.99",
                    skills_covered=["docker", "containers", "devops"]
                ),
                TrainingResource(
                    title="Docker Documentation",
                    provider="Docker",
                    type="tutorial",
                    duration="Self-paced",
                    difficulty="Beginner",
                    url="https://docs.docker.com/",
                    rating=4.8,
                    cost="Free",
                    skills_covered=["docker", "containers", "orchestration"]
                )
            ],
            'project management': [
                TrainingResource(
                    title="Project Management Professional (PMP)",
                    provider="PMI",
                    type="certification",
                    duration="3-6 months",
                    difficulty="Advanced",
                    url="https://www.pmi.org/certifications/types/project-management-pmp",
                    rating=4.6,
                    cost="$555-$800",
                    skills_covered=["project management", "leadership", "planning"]
                ),
                TrainingResource(
                    title="Google Project Management Certificate",
                    provider="Coursera",
                    type="course",
                    duration="6 months",
                    difficulty="Beginner",
                    url="https://www.coursera.org/professional-certificates/google-project-management",
                    rating=4.8,
                    cost="Free (with certificate)",
                    skills_covered=["project management", "agile", "scrum"]
                )
            ],
            'data science': [
                TrainingResource(
                    title="Data Science Professional Certificate",
                    provider="IBM",
                    type="course",
                    duration="11 months",
                    difficulty="Beginner",
                    url="https://www.coursera.org/professional-certificates/ibm-data-science",
                    rating=4.6,
                    cost="Free (with certificate)",
                    skills_covered=["data science", "python", "machine learning"]
                ),
                TrainingResource(
                    title="Kaggle Learn",
                    provider="Kaggle",
                    type="tutorial",
                    duration="Self-paced",
                    difficulty="Beginner",
                    url="https://www.kaggle.com/learn",
                    rating=4.7,
                    cost="Free",
                    skills_covered=["data science", "python", "visualization"]
                )
            ]
        }
        
        return resources
    
    def get_resources_for_skill(self, skill_name: str) -> List[TrainingResource]:
        """Get training resources for a specific skill"""
        skill_key = skill_name.lower()
        
        # Direct match
        if skill_key in self.resources_db:
            return self.resources_db[skill_key]
        
        # Partial match
        for key in self.resources_db:
            if skill_key in key or key in skill_key:
                return self.resources_db[key]
        
        # Return general resources if no specific match
        return self._get_general_resources()
    
    def _get_general_resources(self) -> List[TrainingResource]:
        """Get general learning resources"""
        return [
            TrainingResource(
                title="LinkedIn Learning",
                provider="LinkedIn",
                type="course",
                duration="Varies",
                difficulty="All levels",
                url="https://www.linkedin.com/learning/",
                rating=4.5,
                cost="Subscription",
                skills_covered=["business", "technology", "creative"]
            ),
            TrainingResource(
                title="Pluralsight",
                provider="Pluralsight",
                type="course",
                duration="Varies",
                difficulty="All levels",
                url="https://www.pluralsight.com/",
                rating=4.4,
                cost="Subscription",
                skills_covered=["technology", "development", "it ops"]
            )
        ]
    
    def create_learning_path(self, skill_name: str, current_level: str, target_level: str) -> LearningPath:
        """Create a personalized learning path for a skill"""
        resources = self.get_resources_for_skill(skill_name)
        
        # Filter resources by difficulty
        if current_level.lower() == 'beginner':
            filtered_resources = [r for r in resources if r.difficulty in ['Beginner', 'Intermediate']]
        elif current_level.lower() == 'intermediate':
            filtered_resources = [r for r in resources if r.difficulty in ['Intermediate', 'Advanced']]
        else:
            filtered_resources = resources
        
        # Sort by rating
        filtered_resources.sort(key=lambda x: x.rating, reverse=True)
        
        # Create milestones
        milestones = self._generate_milestones(skill_name, current_level, target_level)
        
        # Estimate duration
        estimated_duration = self._estimate_duration(filtered_resources, current_level, target_level)
        
        return LearningPath(
            skill_name=skill_name,
            current_level=current_level,
            target_level=target_level,
            estimated_duration=estimated_duration,
            resources=filtered_resources[:5],  # Top 5 resources
            milestones=milestones
        )
    
    def _generate_milestones(self, skill_name: str, current_level: str, target_level: str) -> List[str]:
        """Generate learning milestones"""
        milestones = []
        
        if current_level.lower() == 'not present':
            milestones.append(f"Complete introductory {skill_name} course")
            milestones.append(f"Build first {skill_name} project")
            milestones.append(f"Understand core {skill_name} concepts")
        elif current_level.lower() == 'beginner':
            milestones.append(f"Master intermediate {skill_name} concepts")
            milestones.append(f"Complete advanced {skill_name} projects")
            milestones.append(f"Get {skill_name} certification (if available)")
        
        if target_level.lower() in ['intermediate', 'advanced']:
            milestones.append(f"Apply {skill_name} in real-world scenarios")
            milestones.append(f"Contribute to {skill_name} community projects")
            milestones.append(f"Mentor others in {skill_name}")
        
        return milestones
    
    def _estimate_duration(self, resources: List[TrainingResource], current_level: str, target_level: str) -> str:
        """Estimate learning duration"""
        if not resources:
            return "Unknown"
        
        # Simple estimation based on resource durations
        total_hours = 0
        for resource in resources:
            if 'hour' in resource.duration.lower():
                try:
                    hours = int(resource.duration.split()[0])
                    total_hours += hours
                except:
                    total_hours += 20  # Default estimate
            elif 'week' in resource.duration.lower():
                try:
                    weeks = int(resource.duration.split()[0])
                    total_hours += weeks * 10  # Assume 10 hours per week
                except:
                    total_hours += 40
            elif 'month' in resource.duration.lower():
                try:
                    months = int(resource.duration.split()[0])
                    total_hours += months * 40  # Assume 40 hours per month
                except:
                    total_hours += 80
        
        # Adjust based on level progression
        if current_level.lower() == 'not present':
            multiplier = 1.5
        elif current_level.lower() == 'beginner':
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        adjusted_hours = total_hours * multiplier
        
        if adjusted_hours < 40:
            return f"{int(adjusted_hours)} hours"
        elif adjusted_hours < 160:
            return f"{int(adjusted_hours/40)} weeks"
        else:
            return f"{int(adjusted_hours/160)} months"
    
    def get_career_specific_resources(self, career_path: str) -> List[TrainingResource]:
        """Get resources specific to a career path"""
        career_resources = []
        
        # Career-specific resource mappings
        career_mappings = {
            'Software Engineer': ['python', 'javascript', 'react', 'docker'],
            'Data Scientist': ['python', 'machine learning', 'data science'],
            'Product Manager': ['project management'],
            'DevOps Engineer': ['docker', 'aws'],
            'Full Stack Developer': ['python', 'javascript', 'react']
        }
        
        if career_path in career_mappings:
            for skill in career_mappings[career_path]:
                career_resources.extend(self.get_resources_for_skill(skill))
        
        # Remove duplicates and sort by rating
        unique_resources = []
        seen_titles = set()
        
        for resource in career_resources:
            if resource.title not in seen_titles:
                unique_resources.append(resource)
                seen_titles.add(resource.title)
        
        unique_resources.sort(key=lambda x: x.rating, reverse=True)
        return unique_resources[:10]  # Return top 10


if __name__ == "__main__":
    # Test the training resource manager
    manager = TrainingResourceManager()
    
    # Test getting resources for a skill
    python_resources = manager.get_resources_for_skill('python')
    print(f"Found {len(python_resources)} Python resources")
    
    # Test creating a learning path
    learning_path = manager.create_learning_path('python', 'Beginner', 'Advanced')
    print(f"Learning path for Python: {learning_path.estimated_duration}")
    print(f"Milestones: {learning_path.milestones}")
