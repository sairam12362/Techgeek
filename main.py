from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import os
import json
import hashlib
import tempfile
from datetime import datetime, timedelta
import uuid
from pathlib import Path

from ai_evaluator import AIResumeEvaluator
from resume_parser import ResumeParser

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./vidyamitra.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Profile information
    skills = Column(Text, default="[]")  # JSON string
    experience = Column(Text, default="")
    career_goals = Column(Text, default="")
    
    # Relationships
    resume_analyses = relationship("ResumeAnalysis", back_populates="user")
    sessions = relationship("Session", back_populates="user")

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Analysis data (JSON strings)
    score_data = Column(Text, nullable=False)
    resume_data = Column(Text, nullable=False)
    skill_analysis = Column(Text, nullable=False)
    career_recommendations = Column(Text, nullable=False)
    improvement_suggestions = Column(Text, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="resume_analyses")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    skills: List[str] = []
    experience: str = ""
    career_goals: str = ""
    
    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    id: int
    timestamp: datetime
    score_data: Dict[str, Any]
    resume_data: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    career_recommendations: List[Dict[str, Any]]
    improvement_suggestions: List[str]
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="VidyāMitra AI Career Agent", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Fallback for development
    from fastapi.staticfiles import StaticFiles
    import os
    if not os.path.exists("static"):
        os.makedirs("static")
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Security
security = HTTPBearer()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_session(db: Session, user_id: int) -> str:
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    db_session = Session(
        session_id=session_id,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    
    return session_id

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    
    # Find session
    session = db.query(Session).filter(Session.session_id == token).first()
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# API Routes
@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/api/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create session
    session_id = create_session(db, user.id)
    
    return {
        "message": "User registered successfully",
        "session_id": session_id,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "skills": json.loads(user.skills) if user.skills else [],
            "experience": user.experience,
            "career_goals": user.career_goals
        }
    }

@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create session
    session_id = create_session(db, user.id)
    
    return {
        "message": "Login successful",
        "session_id": session_id,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "skills": json.loads(user.skills) if user.skills else [],
            "experience": user.experience,
            "career_goals": user.career_goals
        }
    }

@app.post("/api/logout")
async def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Remove all sessions for this user
    db.query(Session).filter(Session.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "Logout successful"}

@app.get("/api/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "skills": json.loads(current_user.skills) if current_user.skills else [],
        "experience": current_user.experience,
        "career_goals": current_user.career_goals,
        "created_at": current_user.created_at
    }

@app.put("/api/profile")
async def update_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if "skills" in profile_data:
        current_user.skills = json.dumps(profile_data["skills"])
    if "experience" in profile_data:
        current_user.experience = profile_data["experience"]
    if "career_goals" in profile_data:
        current_user.career_goals = profile_data["career_goals"]
    
    db.commit()
    
    return {"message": "Profile updated successfully"}

@app.get("/api/analyses")
async def get_analyses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    analyses = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == current_user.id
    ).order_by(ResumeAnalysis.timestamp.desc()).limit(10).all()
    
    return [
        {
            "id": analysis.id,
            "timestamp": analysis.timestamp,
            "score_data": json.loads(analysis.score_data),
            "resume_data": json.loads(analysis.resume_data),
            "skill_analysis": json.loads(analysis.skill_analysis),
            "career_recommendations": json.loads(analysis.career_recommendations),
            "improvement_suggestions": json.loads(analysis.improvement_suggestions)
        }
        for analysis in analyses
    ]

@app.post("/api/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be PDF, DOCX, or TXT"
        )
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Initialize simple analyzer (no AI dependency)
        from simple_analyzer import SimpleResumeAnalyzer
        analyzer = SimpleResumeAnalyzer()
        
        # Perform analysis
        result = analyzer.analyze_resume(tmp_file_path)
        
        # Save analysis to database
        analysis = ResumeAnalysis(
            user_id=current_user.id,
            score_data=json.dumps(result['score']),
            resume_data=json.dumps(result['resume_data']),
            skill_analysis=json.dumps(result['skill_analysis']),
            career_recommendations=json.dumps(result['career_recommendations']),
            improvement_suggestions=json.dumps(result['improvement_suggestions'])
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Update user profile with latest analysis data
        current_user.skills = json.dumps(result['resume_data']['skills'])
        db.commit()
        db.refresh(current_user)
        
        return {
            "id": analysis.id,
            "timestamp": analysis.timestamp,
            "score_data": result['score'],
            "resume_data": result['resume_data'],
            "skill_analysis": result['skill_analysis'],
            "career_recommendations": result['career_recommendations'],
            "improvement_suggestions": result['improvement_suggestions']
        }
        
    except Exception as e:
        # Log the error for debugging
        print(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_file_path)
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
