# VidyāMitra AI Agent

🤖 **AI-Powered Resume Analysis and Career Guidance Platform**

## ✨ Features

### � Resume Analysis
- **Smart Parsing**: Extract skills, experience, and education from PDF, DOCX, TXT
- **AI Scoring**: Comprehensive resume scoring with detailed breakdown
- **Skill Assessment**: Detailed skill proficiency analysis with levels
- **Real-time Processing**: Instant analysis and feedback

### 🎯 Career Recommendations
- **Personalized Matches**: Career suggestions based on your skills
- **Salary Insights**: Realistic salary ranges for different roles
- **Growth Potential**: Career growth opportunities
- **Skill Gap Analysis**: Missing skills and learning resources

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Beautiful, modern interface
- **Responsive Layout**: Works perfectly on all devices
- **Smooth Animations**: Interactive elements and transitions
- **Dark Theme**: Professional dark color scheme

### 👤 User Management
- **Secure Authentication**: User registration and login
- **Profile Management**: Edit skills, experience, goals
- **Analysis History**: Track all your resume analyses
- **Data Persistence**: All data saved securely

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Powerful ORM for database management
- **SQLite**: Lightweight, reliable database
- **Pydantic**: Data validation and serialization

### Frontend
- **Vanilla JavaScript**: Modern ES6+ features
- **CSS3**: Advanced styling with animations
- **HTML5**: Semantic, accessible markup
- **No Framework Dependencies**: Lightweight and fast

### AI/ML
- **OpenAI GPT-4**: Advanced AI analysis
- **Intelligent Fallbacks**: Works even without AI
- **Skill Categorization**: Technical and soft skills
- **Career Matching**: Algorithm-based recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key (optional, has fallback)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sairam12362/Techgeek.git
   cd Techgeek
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python start.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:8000`

## 📁 Project Structure

```
vidyamitra-ai-agent/
├── main.py                 # FastAPI backend server
├── simple_analyzer.py      # Resume analysis engine
├── resume_parser.py         # Resume parsing logic
├── ai_evaluator.py         # AI analysis (backup)
├── database.py            # Database models and setup
├── start.py               # Application startup script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── GITHUB_SETUP.md        # GitHub setup guide
└── static/                # Frontend assets
    ├── index.html         # Main application UI
    ├── styles.css          # Application styling
    └── script.js          # Frontend JavaScript logic
```

## 🎯 How It Works

### 1. Resume Upload
- Users upload PDF, DOCX, or TXT files
- Files are parsed and processed securely
- Support for multiple file formats

### 2. AI Analysis
- Resume content is analyzed using AI
- Skills are extracted and categorized
- Experience and education are parsed

### 3. Scoring System
- Overall resume score (0-100)
- Section-wise scoring (Skills, Experience, Education)
- Strengths and weaknesses identification

### 4. Career Matching
- Skills matched against career paths
- Personalized recommendations generated
- Salary and growth insights provided

### 5. Improvement Suggestions
- Specific, actionable recommendations
- Skill gap analysis
- Learning resources and tips

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
```

### Database Setup
- SQLite database created automatically
- No additional configuration required
- Data persistence included

## 📊 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile

### Resume Analysis
- `POST /api/analyze-resume` - Analyze resume
- `GET /api/analyses` - Get analysis history

### Profile Management
- `PUT /api/profile` - Update profile
- `GET /api/logout` - User logout

## 🎨 Features Showcase

### Resume Analysis Features
- ✅ PDF, DOCX, TXT file support
- ✅ Real-time parsing and analysis
- ✅ Skill proficiency levels
- ✅ Experience-based scoring
- ✅ Education verification

### Career Recommendations
- ✅ 5+ career path suggestions
- ✅ Match percentage scoring
- ✅ Salary range insights
- ✅ Growth potential analysis
- ✅ Missing skills identification

### User Experience
- ✅ Beautiful, modern interface
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Progress tracking
- ✅ Error handling

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Test your changes thoroughly
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support or questions:

1. Check the [Issues](https://github.com/sairam12362/Techgeek/issues) page
2. Create a new issue with detailed description
3. Include steps to reproduce any bugs

## 🌟 Acknowledgments

- OpenAI for powerful AI capabilities
- FastAPI for excellent web framework
- All contributors and users

---

**Built with ❤️ for job seekers and career changers**
- **Actionable Improvement Suggestions** tailored to each resume

### 💾 Robust Backend
- **FastAPI** for high-performance API endpoints
- **SQL Database** for secure user data storage
- **JWT Authentication** with session management
- **File Upload Support** for PDF, DOCX, and TXT
- **RESTful API** with comprehensive documentation

### 🎨 Modern UI/UX
- **Animated Backgrounds** with floating particles
- **Mouse-Responsive Elements** with 3D tilt effects
- **Gradient Animations** that shift over time
- **Toast Notifications** for user feedback
- **Loading States** with smooth transitions

## 🛠️ Technology Stack

### Frontend
- **JavaScript (ES6+)** - Modern vanilla JavaScript
- **CSS3** - Advanced animations and glass morphism
- **HTML5** - Semantic markup
- **Font Awesome** - Icon library

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)
- **Pydantic** - Data validation
- **OpenAI GPT-4** - AI analysis engine

### AI/ML
- **OpenAI API** - Advanced language model
- **Resume Parsing** - Intelligent text extraction
- **Skill Analysis** - AI-powered categorization
- **Career Matching** - Dynamic recommendation engine

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

3. **Start the application**
```bash
python start.py
```

4. **Open your browser**
Navigate to `http://localhost:8000`

## 📁 Project Structure

```
vidyamitra-ai-agent/
├── main.py                 # FastAPI application
├── start.py               # Startup script
├── ai_evaluator.py        # AI analysis engine
├── resume_parser.py       # Resume parsing logic
├── requirements.txt       # Python dependencies
├── static/               # Frontend assets
│   ├── index.html       # Main HTML file
│   ├── styles.css       # Advanced CSS with animations
│   └── script.js        # Interactive JavaScript
├── vidyamitra.db        # SQLite database (auto-created)
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)

## 📊 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Resume Analysis
- `POST /api/analyze-resume` - Upload and analyze resume
- `GET /api/analyses` - Get analysis history

### Documentation
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## 🎯 Key Features

### AI Resume Analysis
- **Skill Extraction**: Automatically identifies and categorizes skills
- **Proficiency Assessment**: Estimates skill levels from experience
- **Career Matching**: Matches profile to suitable career paths
- **Gap Analysis**: Identifies missing skills for target roles
- **Improvement Suggestions**: Provides actionable recommendations

### Interactive Frontend
- **Mouse Tracking**: Floating elements follow cursor movement
- **3D Tilt Effects**: Cards respond to mouse hover
- **Smooth Transitions**: All interactions are animated
- **Responsive Design**: Adapts to all screen sizes
- **Real-time Updates**: Live progress tracking

### Data Management
- **Secure Storage**: User data encrypted in SQL database
- **Session Management**: Secure JWT-based authentication
- **Analysis History**: Track resume improvements over time
- **Profile Management**: Update skills and career goals

---

**Built with ❤️ using cutting-edge web technologies and AI**
=======
# Techgeek
>>>>>>> 45d106f40d602d201eccb5d8c7547da994183532
