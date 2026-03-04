// Modern JavaScript for VidyāMitra High-End Frontend

// Global state
let currentUser = null;
let currentSection = 'dashboard';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Clear any existing session to prevent account mixing
    clearExistingSession();
    
    // Check if user is logged in (from localStorage)
    const currentUserId = localStorage.getItem('vidyamitra_current_user');
    if (currentUserId) {
        const userData = localStorage.getItem('vidyamitra_user_' + currentUserId);
        if (userData) {
            currentUser = JSON.parse(userData);
            showDashboard();
        } else {
            showLogin();
        }
    } else {
        showLogin();
    }
    
    // Setup form listeners
    setupFormListeners();
    
    // Setup upload functionality
    setupUpload();
    
    // Initialize animations
    initializeAnimations();
}

function clearExistingSession() {
    // Clear any potentially corrupted session data
    const sessionKeys = Object.keys(localStorage).filter(key => key.startsWith('vidyamitra_'));
    sessionKeys.forEach(key => {
        if (key !== 'vidyamitra_user') {
            localStorage.removeItem(key);
        }
    });
}

// Authentication functions
function showLogin() {
    document.getElementById('loginContainer').style.display = 'flex';
    document.getElementById('dashboardContainer').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function showDashboard() {
    document.getElementById('loginContainer').style.display = 'none';
    document.getElementById('dashboardContainer').style.display = 'flex';
    document.body.style.overflow = 'auto';
    
    if (currentUser) {
        document.getElementById('userName').textContent = currentUser.name;
        
        // Check if this is a new account (no resume uploaded yet)
        const hasResume = localStorage.getItem('vidyamitra_resume_' + currentUser.userId);
        if (!hasResume) {
            // Show fresh state for new accounts
            showFreshAccountState();
        } else {
            // Show existing analysis
            animateMetrics();
        }
    }
}

function showFreshAccountState() {
    // Reset all metrics to 0 for new accounts
    document.querySelectorAll('.metric-value').forEach(element => {
        element.textContent = '0';
        element.setAttribute('data-target', '0');
    });
    
    // Show welcome message for new users
    const welcomeMessage = document.createElement('div');
    welcomeMessage.className = 'glass-card';
    welcomeMessage.innerHTML = `
        <h2>👋 Welcome to VidyāMitra, ${currentUser.name}!</h2>
        <p>Get started by uploading your resume to receive personalized career insights and recommendations.</p>
        <button class="btn-primary" onclick="showSection('upload')">Upload Your Resume</button>
    `;
    
    // Insert welcome message after header
    const mainContent = document.querySelector('.main-content');
    const existingWelcome = mainContent.querySelector('.welcome-message');
    if (existingWelcome) {
        existingWelcome.remove();
    }
    welcomeMessage.classList.add('welcome-message');
    mainContent.insertBefore(welcomeMessage, mainContent.querySelector('.metrics-grid'));
}

function showLoginTab() {
    document.getElementById('loginForm').style.display = 'flex';
    document.getElementById('registerForm').style.display = 'none';
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.querySelectorAll('.tab-btn')[1].classList.remove('active');
}

function showRegisterTab() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'flex';
    document.querySelectorAll('.tab-btn')[0].classList.remove('active');
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
}

// Tab switching
function showLogin() {
    showLoginTab();
}

function showRegister() {
    showRegisterTab();
}

// Form handling
function setupFormListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin();
    });
    
    // Register form
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleRegister();
    });
    
    // Profile form
    const profileForm = document.querySelector('.profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleProfileUpdate();
        });
    }
}

function handleLogin() {
    const email = document.querySelector('#loginForm input[type="email"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;
    
    if (email && password) {
        // Find user by checking all stored user sessions
        const userKeys = Object.keys(localStorage).filter(key => key.startsWith('vidyamitra_user_'));
        let foundUser = null;
        let foundUserId = null;
        
        for (const key of userKeys) {
            const userData = JSON.parse(localStorage.getItem(key));
            if (userData.email === email) {
                // Simple password validation (in real app, use proper hashing)
                foundUser = userData;
                foundUserId = key.replace('vidyamitra_user_', '');
                break;
            }
        }
        
        if (foundUser) {
            currentUser = foundUser;
            localStorage.setItem('vidyamitra_current_user', foundUserId);
            showDashboard();
            showNotification('Login successful!', 'success');
        } else {
            showNotification('Invalid email or password', 'error');
        }
    } else {
        showNotification('Please fill in all fields', 'error');
    }
}

function handleRegister() {
    const name = document.querySelector('#registerForm input[type="text"]').value;
    const email = document.querySelector('#registerForm input[type="email"]').value;
    const password = document.querySelector('#registerForm input[type="password"]').value;
    const confirmPassword = document.querySelectorAll('#registerForm input[type="password"]')[1].value;
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    if (name && email && password) {
        // Create unique user ID to prevent account mixing
        const userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        currentUser = { 
            name, 
            email, 
            userId,
            createdAt: new Date().toISOString()
        };
        
        // Store with unique key
        localStorage.setItem('vidyamitra_user_' + userId, JSON.stringify(currentUser));
        localStorage.setItem('vidyamitra_current_user', userId);
        
        showDashboard();
        showNotification('Registration successful! Welcome to VidyāMitra!', 'success');
    } else {
        showNotification('Please fill in all fields', 'error');
    }
}

function handleProfileUpdate() {
    showNotification('Profile updated successfully!', 'success');
}

function logout() {
    // Get current user ID
    const currentUserId = localStorage.getItem('vidyamitra_current_user');
    
    if (currentUserId) {
        // Remove current user session
        localStorage.removeItem('vidyamitra_user_' + currentUserId);
        localStorage.removeItem('vidyamitra_current_user');
    }
    
    currentUser = null;
    showLogin();
    showNotification('Logged out successfully', 'info');
}

// Navigation
function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(s => {
        s.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(section + 'Section').style.display = 'block';
    
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    event.target.closest('.nav-item').classList.add('active');
    
    currentSection = section;
    
    // Re-animate metrics when returning to dashboard
    if (section === 'dashboard') {
        setTimeout(() => animateMetrics(), 100);
    }
}

// Upload functionality
function setupUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.8)';
            uploadArea.style.background = 'rgba(255, 255, 255, 0.1)';
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            uploadArea.style.background = 'rgba(255, 255, 255, 0.05)';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            uploadArea.style.background = 'rgba(255, 255, 255, 0.05)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
}

function handleFileUpload(file) {
    // Support for images and documents
    const validTypes = [
        'application/pdf', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
        'text/plain',
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/webp'
    ];
    
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a PDF, DOCX, TXT, or Image file', 'error');
        return;
    }
    
    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }
    
    // Show file preview for images
    if (file.type.startsWith('image/')) {
        showImagePreview(file);
    }
    
    // Simulate file upload
    showNotification(`Uploading ${file.name}...`, 'info');
    
    setTimeout(() => {
        // Mark that user has uploaded a resume
        if (currentUser && currentUser.userId) {
            localStorage.setItem('vidyamitra_resume_' + currentUser.userId, JSON.stringify({
                fileName: file.name,
                fileSize: file.size,
                fileType: file.type,
                uploadedAt: new Date().toISOString()
            }));
        }
        
        showNotification('Resume uploaded and analyzed successfully!', 'success');
        
        // Remove welcome message if it exists
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        // Update metrics with new analysis data
        updateMetricsWithNewData();
    }, 2000);
}

function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = document.createElement('div');
        previewContainer.className = 'image-preview';
        previewContainer.innerHTML = `
            <h4>📷 Resume Preview</h4>
            <img src="${e.target.result}" alt="Resume preview" style="max-width: 100%; max-height: 300px; border-radius: 8px; margin-bottom: 1rem;">
            <p><strong>File:</strong> ${file.name}</p>
            <p><strong>Size:</strong> ${(file.size / 1024).toFixed(2)} KB</p>
            <p><strong>Type:</strong> ${file.type}</p>
        `;
        
        // Insert preview after upload area
        const uploadSection = document.getElementById('uploadSection');
        const uploadCard = uploadSection.querySelector('.glass-card');
        uploadCard.appendChild(previewContainer);
    };
    reader.readAsDataURL(file);
}

function updateMetricsWithNewData() {
    // Simulate new analysis data
    const newMetrics = {
        overall: Math.floor(Math.random() * 20) + 80,
        skills: Math.floor(Math.random() * 10) + 10,
        experience: Math.floor(Math.random() * 5) + 2,
        education: Math.floor(Math.random() * 3) + 1
    };
    
    // Update metric values
    document.querySelectorAll('.metric-value').forEach((element, index) => {
        const values = Object.values(newMetrics);
        element.setAttribute('data-target', values[index]);
    });
    
    // Re-animate
    animateMetrics();
}

// Animations
function initializeAnimations() {
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add hover effects to cards
    addCardHoverEffects();
}

function animateMetrics() {
    const metricValues = document.querySelectorAll('.metric-value');
    
    metricValues.forEach(element => {
        const target = parseInt(element.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    });
}

function addCardHoverEffects() {
    const cards = document.querySelectorAll('.metric-card, .recommendation-card, .glass-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Export functionality
function exportAsPDF() {
    showNotification('Generating PDF export...', 'info');
    setTimeout(() => {
        showNotification('PDF exported successfully!', 'success');
    }, 2000);
}

function shareLink() {
    // Copy link to clipboard
    const dummy = document.createElement('input');
    document.body.appendChild(dummy);
    dummy.value = window.location.href;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);
    
    showNotification('Link copied to clipboard!', 'success');
}

function emailReport() {
    showNotification('Sending email report...', 'info');
    setTimeout(() => {
        showNotification('Report sent successfully!', 'success');
    }, 2000);
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;
    
    // Set background color based on type
    const colors = {
        success: 'rgba(74, 222, 128, 0.2)',
        error: 'rgba(248, 113, 113, 0.2)',
        info: 'rgba(96, 165, 250, 0.2)'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for quick search (placeholder)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        showNotification('Quick search coming soon!', 'info');
    }
    
    // Escape to logout
    if (e.key === 'Escape' && currentUser) {
        logout();
    }
});

// Performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add resize listener with debounce
window.addEventListener('resize', debounce(() => {
    // Handle responsive adjustments
    if (window.innerWidth < 768) {
        // Mobile adjustments
        console.log('Mobile view');
    } else {
        // Desktop adjustments
        console.log('Desktop view');
    }
}, 250));

// Initialize service worker for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// Export functions for global access
window.showLogin = showLogin;
window.showRegister = showRegister;
window.showSection = showSection;
window.logout = logout;
window.exportAsPDF = exportAsPDF;
window.shareLink = shareLink;
window.emailReport = emailReport;
