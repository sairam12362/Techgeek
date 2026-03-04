// Advanced JavaScript with Mouse Interactions and Modern Features

class VidyamitraApp {
    constructor() {
        this.currentUser = null;
        this.sessionId = localStorage.getItem('sessionId') || null;
        this.apiBase = window.location.origin + '/api';
        this.currentAnalysis = null;
        this.mouseX = 0;
        this.mouseY = 0;
        
        this.init();
    }

    async init() {
        console.log('Initializing Vidyamitra App...');
        
        this.setupEventListeners();
        this.setupMouseTracking();
        this.setupTiltEffect();
        
        // Force hide navbar immediately
        console.log('Hiding navbar on init...');
        this.hideNavigation();
        
        // Check if user is logged in
        if (this.sessionId) {
            console.log('User has session, validating...');
            await this.validateSession();
        } else {
            console.log('No session found, showing login...');
            this.showSection('loginSection');
        }
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                this.showSection(section + 'Section');
                this.setActiveNav(link);
            });
        });

        // Auth tabs
        document.querySelectorAll('.auth-tabs .tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = btn.dataset.tab;
                this.switchAuthTab(tab);
            });
        });

        // Auth forms
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });

        // Profile form
        document.getElementById('profileForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.updateProfile();
        });

        // File upload
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const browseBtn = document.getElementById('browseBtn');

        browseBtn.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.logout();
        });

        // Mobile menu toggle
        document.getElementById('navToggle').addEventListener('click', () => {
            document.getElementById('navMenu').classList.toggle('active');
            document.getElementById('navToggle').classList.toggle('active');
        });

        // Analysis tabs
        document.querySelectorAll('.analysis-tabs .tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = btn.dataset.tab;
                this.switchAnalysisTab(tab);
            });
        });
    }

    setupMouseTracking() {
        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
            // Mouse tracking for future features
        });
    }

    setupTiltEffect() {
        const cards = document.querySelectorAll('[data-tilt]');
        
        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
            });
        });
    }

    switchAuthTab(tab) {
        document.querySelectorAll('.auth-tabs .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        document.querySelectorAll('.auth-form').forEach(form => {
            form.classList.remove('active');
        });
        document.getElementById(tab + 'Form').classList.add('active');
    }

    switchAnalysisTab(tab) {
        document.querySelectorAll('.analysis-tabs .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(tab + 'Tab').classList.add('active');
    }

    showSection(sectionId) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
    }

    setActiveNav(activeLink) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            this.showLoading();
            const response = await fetch(`${this.apiBase}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.sessionId = data.session_id;
                localStorage.setItem('sessionId', this.sessionId);
                this.currentUser = data.user;
                this.showToast('Login successful!', 'success');
                this.showDashboard();
            } else {
                this.showToast(data.detail || 'Login failed', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async handleRegister() {
        const name = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            this.showToast('Passwords do not match', 'error');
            return;
        }

        if (password.length < 6) {
            this.showToast('Password must be at least 6 characters', 'error');
            return;
        }

        try {
            this.showLoading();
            const response = await fetch(`${this.apiBase}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.sessionId = data.session_id;
                localStorage.setItem('sessionId', this.sessionId);
                this.currentUser = data.user;
                this.showToast('Registration successful!', 'success');
                this.showDashboard();
            } else {
                this.showToast(data.detail || 'Registration failed', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async validateSession() {
        try {
            const response = await fetch(`${this.apiBase}/profile`, {
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.currentUser = data;
                console.log('Session valid, showing dashboard...');
                this.showDashboard();
            } else {
                console.log('Session invalid, hiding navbar...');
                localStorage.removeItem('sessionId');
                this.sessionId = null;
                this.hideNavigation();
                this.showSection('loginSection');
            }
        } catch (error) {
            console.log('Session validation error, hiding navbar...');
            localStorage.removeItem('sessionId');
            this.sessionId = null;
            this.hideNavigation();
            this.showSection('loginSection');
        }
    }

    showNavigation() {
        console.log('Showing navigation...');
        const navbar = document.getElementById('navbar');
        const navMenu = document.getElementById('navMenu');
        const navToggle = document.getElementById('navToggle');
        const mainContent = document.querySelector('.main-content');
        
        if (navbar) {
            console.log('Found navbar, showing it...');
            // Force show with inline styles and !important
            navbar.style.setProperty('display', 'block', 'important');
            navbar.style.setProperty('visibility', 'visible', 'important');
            navbar.style.setProperty('opacity', '1', 'important');
            navbar.style.setProperty('height', 'auto', 'important');
            navbar.style.setProperty('overflow', 'visible', 'important');
            navbar.style.setProperty('position', 'fixed', 'important');
            navbar.style.setProperty('top', '0', 'important');
            navbar.style.setProperty('left', '0', 'important');
            navbar.style.setProperty('right', '0', 'important');
            console.log('Navbar forced to show with !important');
        } else {
            console.log('ERROR: Navbar not found!');
        }
        
        if (mainContent) {
            mainContent.classList.add('navbar-visible');
            console.log('Added navbar-visible class to main content');
        }
        
        if (navMenu) {
            navMenu.style.display = 'flex';
            navMenu.style.flexDirection = 'row';
            navMenu.style.alignItems = 'center';
            navMenu.style.gap = '2rem';
            console.log('Nav menu shown');
        }
        
        if (navToggle) {
            navToggle.style.display = 'none';
        }
        
        // Show all navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.style.display = 'flex';
        });
        
        // Show logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.style.display = 'flex';
        }
        
        console.log('Navigation shown successfully');
    }

    hideNavigation() {
        console.log('Hiding navigation...');
        const navbar = document.getElementById('navbar');
        const navMenu = document.getElementById('navMenu');
        const navToggle = document.getElementById('navToggle');
        const mainContent = document.querySelector('.main-content');
        
        if (navbar) {
            console.log('Found navbar, hiding it...');
            // Force hide with inline styles and !important
            navbar.style.setProperty('display', 'none', 'important');
            navbar.style.setProperty('visibility', 'hidden', 'important');
            navbar.style.setProperty('opacity', '0', 'important');
            navbar.style.setProperty('height', '0', 'important');
            navbar.style.setProperty('overflow', 'hidden', 'important');
            navbar.style.setProperty('position', 'absolute', 'important');
            navbar.style.setProperty('top', '-9999px', 'important');
            navbar.style.setProperty('left', '-9999px', 'important');
            console.log('Navbar forced to hide with !important');
        }
        
        if (mainContent) {
            mainContent.classList.remove('navbar-visible');
        }
        
        if (navMenu) {
            navMenu.style.display = 'none';
        }
        
        if (navToggle) {
            navToggle.style.display = 'flex';
        }
        
        // Hide all navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.style.display = 'none';
        });
        
        // Hide logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.style.display = 'none';
        }
        
        console.log('Navigation hidden successfully');
    }

    showDashboard() {
        document.getElementById('userName').textContent = this.currentUser.name;
        this.showSection('dashboardSection');
        this.loadProfile();
        this.loadAnalysisHistory();
        
        // Show navigation menu after login
        this.showNavigation();
    }

    async loadProfile() {
        try {
            const response = await fetch(`${this.apiBase}/profile`, {
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.currentUser = data;
                this.updateProfileUI();
                
                // Display latest analysis if available
                if (data.skills && data.skills.length > 0) {
                    console.log('Displaying latest analysis from profile:', data.skills);
                    this.displayLatestAnalysis(data.skills);
                }
            }
        } catch (error) {
            console.error('Failed to load profile:', error);
        }
    }

    async displayLatestAnalysis(skillsData) {
        try {
            // Get the most recent analysis
            const response = await fetch(`${this.apiBase}/analyses`, {
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                }
            });

            if (response.ok) {
                const analyses = await response.json();
                if (analyses && analyses.length > 0) {
                    const latestAnalysis = analyses[0];
                    console.log('Latest analysis found:', latestAnalysis);
                    
                    // Display the latest analysis results
                    if (latestAnalysis.skill_analysis && latestAnalysis.skill_analysis.skill_proficiency) {
                        this.displaySkillsWithProficiency(latestAnalysis.resume_data.skills, latestAnalysis.skill_analysis.skill_proficiency);
                    } else {
                        this.displaySkills(latestAnalysis.resume_data.skills);
                    }
                    
                    this.displayCareerRecommendations(latestAnalysis.career_recommendations);
                    this.displaySuggestions(latestAnalysis.improvement_suggestions);
                }
            }
        } catch (error) {
            console.error('Failed to load analyses:', error);
        }
    }

    updateProfileUI() {
        document.getElementById('profileSkills').value = this.currentUser.skills.join(', ');
        document.getElementById('profileExperience').value = this.currentUser.experience;
        document.getElementById('profileGoals').value = this.currentUser.career_goals;
        
        // Update stats
        document.getElementById('profileSkillsCount').textContent = this.currentUser.skills.length;
    }

    async updateProfile() {
        const skills = document.getElementById('profileSkills').value
            .split(',')
            .map(skill => skill.trim())
            .filter(skill => skill);
        const experience = document.getElementById('profileExperience').value;
        const career_goals = document.getElementById('profileGoals').value;

        try {
            this.showLoading();
            const response = await fetch(`${this.apiBase}/profile`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.sessionId}`
                },
                body: JSON.stringify({ skills, experience, career_goals })
            });

            if (response.ok) {
                this.showToast('Profile updated successfully!', 'success');
                this.loadProfile();
            } else {
                this.showToast('Failed to update profile', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async handleFileUpload(file) {
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
        
        if (!validTypes.includes(file.type)) {
            this.showToast('Please upload a PDF, DOCX, or TXT file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            this.showUploadProgress();
            
            const response = await fetch(`${this.apiBase}/analyze-resume`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                this.currentAnalysis = data;
                this.displayAnalysisResults(data);
                this.showToast('Resume analysis completed!', 'success');
                this.loadAnalysisHistory();
            } else {
                this.showToast(data.detail || 'Analysis failed', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideUploadProgress();
        }
    }

    showUploadProgress() {
        document.getElementById('uploadProgress').classList.remove('hidden');
        document.querySelector('.upload-content').classList.add('hidden');
        
        // Animate progress bar
        let progress = 0;
        const progressFill = document.getElementById('progressFill');
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 500);

        // Store interval ID to clear later
        this.progressInterval = interval;
    }

    hideUploadProgress() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        // Complete the progress
        document.getElementById('progressFill').style.width = '100%';
        
        setTimeout(() => {
            document.getElementById('uploadProgress').classList.add('hidden');
            document.querySelector('.upload-content').classList.remove('hidden');
            document.getElementById('progressFill').style.width = '0%';
        }, 500);
    }

    displayAnalysisResults(analysis) {
        document.getElementById('resultsSection').classList.remove('hidden');
        
        // Update score cards
        const score = analysis.score_data.overall_score;
        document.getElementById('overallScore').textContent = `${score}/100`;
        document.getElementById('scoreProgress').style.width = `${score}%`;
        
        document.getElementById('skillsCount').textContent = analysis.resume_data.skills.length;
        document.getElementById('experienceCount').textContent = analysis.resume_data.work_experience.length;
        document.getElementById('educationCount').textContent = analysis.resume_data.education.length;

        // Update strengths and weaknesses
        this.displayStrengthsWeaknesses(analysis.score_data);
        
        // Update skills
        this.displaySkills(analysis.resume_data.skills);
        
        // Update career recommendations
        this.displayCareers(analysis.career_recommendations);
        
        // Update suggestions
        this.displaySuggestions(analysis.improvement_suggestions);

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    displayStrengthsWeaknesses(scoreData) {
        const strengthsList = document.getElementById('strengthsList');
        const weaknessesList = document.getElementById('weaknessesList');
        
        strengthsList.innerHTML = '';
        weaknessesList.innerHTML = '';
        
        scoreData.strengths.forEach(strength => {
            const li = document.createElement('li');
            li.textContent = strength;
            strengthsList.appendChild(li);
        });
        
        scoreData.weaknesses.forEach(weakness => {
            const li = document.createElement('li');
            li.textContent = weakness;
            weaknessesList.appendChild(li);
        });
    }

    displaySkillsWithProficiency(skills, proficiencyData) {
        const container = document.getElementById('skillsContainer');
        container.innerHTML = '';
        
        if (proficiencyData && typeof proficiencyData === 'object') {
            Object.entries(proficiencyData).forEach(([skillName, skillData]) => {
                const skillTag = document.createElement('div');
                skillTag.className = 'skill-tag';
                
                const level = skillData.level || 'Unknown';
                const confidence = skillData.confidence || 0;
                const years = skillData.years_experience || 0;
                
                skillTag.innerHTML = `
                    <strong>${skillName}</strong>
                    <div class="skill-details">
                        <span class="skill-level">Level: ${level}</span>
                        <span class="skill-confidence">Confidence: ${(confidence * 100).toFixed(1)}%</span>
                        ${years > 0 ? `<span class="skill-years">${years} years</span>` : ''}
                    </div>
                `;
                
                container.appendChild(skillTag);
            });
        } else {
            // Fallback to simple skill display
            skills.forEach(skill => {
                const skillTag = document.createElement('div');
                skillTag.className = 'skill-tag';
                skillTag.textContent = skill.name || skill;
                container.appendChild(skillTag);
            });
        }
    }

    displaySkills(skills) {
        const container = document.getElementById('skillsContainer');
        container.innerHTML = '';
        
        skills.forEach(skill => {
            const skillTag = document.createElement('div');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill.name || skill;
            container.appendChild(skillTag);
        });
    }

    displayCareers(careers) {
        const container = document.getElementById('careersContainer');
        container.innerHTML = '';
        
        careers.slice(0, 5).forEach(career => {
            const card = document.createElement('div');
            card.className = 'career-card';
            card.innerHTML = `
                <div class="career-title">
                    <span>${career.job_title}</span>
                    <span class="match-score">${career.match_score.toFixed(1)}%</span>
                </div>
                <div class="career-details">
                    <div class="career-detail">
                        <span class="career-label">Salary Range</span>
                        <span class="career-value">${career.salary_range}</span>
                    </div>
                    <div class="career-detail">
                        <span class="career-label">Growth Potential</span>
                        <span class="career-value">${career.growth_potential}</span>
                    </div>
                    <div class="career-detail">
                        <span class="career-label">Required Skills</span>
                        <span class="career-value">${career.required_skills.join(', ')}</span>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    displaySuggestions(suggestions) {
        const container = document.getElementById('suggestionsContainer');
        container.innerHTML = '';
        
        suggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                <strong>${index + 1}.</strong> ${suggestion}
            `;
            container.appendChild(item);
        });
    }

    async loadAnalysisHistory() {
        try {
            const response = await fetch(`${this.apiBase}/analyses`, {
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                }
            });

            if (response.ok) {
                const analyses = await response.json();
                this.displayAnalysisHistory(analyses);
                this.updateStats(analyses);
            }
        } catch (error) {
            console.error('Failed to load analysis history:', error);
        }
    }

    displayAnalysisHistory(analyses) {
        const container = document.getElementById('historyContent');
        container.innerHTML = '';
        
        if (analyses.length === 0) {
            container.innerHTML = '<p class="text-center">No analysis history available.</p>';
            return;
        }
        
        analyses.forEach(analysis => {
            const item = document.createElement('div');
            item.className = 'history-item';
            const date = new Date(analysis.timestamp).toLocaleDateString();
            const score = analysis.score_data.overall_score;
            
            item.innerHTML = `
                <div class="history-header">
                    <span class="history-date">${date}</span>
                    <span class="history-score">${score}/100</span>
                </div>
                <div class="history-details">
                    <p><strong>Skills:</strong> ${analysis.resume_data.skills.length} identified</p>
                    <p><strong>Top Career:</strong> ${analysis.career_recommendations[0]?.job_title || 'N/A'}</p>
                </div>
            `;
            container.appendChild(item);
        });
    }

    updateStats(analyses) {
        document.getElementById('analysisCount').textContent = analyses.length;
        
        if (analyses.length > 0) {
            const latestScore = analyses[0].score_data.overall_score;
            document.getElementById('latestScore').textContent = latestScore;
        }
    }

    async logout() {
        try {
            await fetch(`${this.apiBase}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.sessionId}`
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        }
        
        localStorage.removeItem('sessionId');
        this.sessionId = null;
        this.currentUser = null;
        this.showToast('Logged out successfully', 'info');
        
        // Hide navigation after logout
        this.hideNavigation();
        this.showSection('loginSection');
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'times-circle' : 'info-circle';
        
        toast.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VidyamitraApp();
});

// Add some additional interactive effects
document.addEventListener('DOMContentLoaded', () => {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Add ripple effect styles
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
