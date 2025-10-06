// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.bindEvents();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateToggleButton(theme);
    }

    updateToggleButton(theme) {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            const icon = toggle.querySelector('i');
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
    }

    bindEvents() {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggleTheme());
        }
    }
}

// Form Validation
class FormValidator {
    constructor() {
        this.init();
    }

    init() {
        this.bindFormEvents();
    }

    bindFormEvents() {
        // Signup form validation
        const signupForm = document.querySelector('form[action*="signup"]');
        if (signupForm) {
            signupForm.addEventListener('submit', (e) => this.validateSignupForm(e));
        }

        // Login form validation
        const loginForm = document.querySelector('form[action*="login"]');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.validateLoginForm(e));
        }

        // Resume form validation
        const resumeForm = document.querySelector('.resume-form');
        if (resumeForm) {
            resumeForm.addEventListener('submit', (e) => this.validateResumeForm(e));
        }
    }

    validateSignupForm(e) {
        const form = e.target;
        const password = form.querySelector('#password');
        const confirmPassword = form.querySelector('#confirm_password');
        const email = form.querySelector('#email');

        let isValid = true;

        // Email validation
        if (!this.isValidEmail(email.value)) {
            this.showError(email, 'Please enter a valid email address');
            isValid = false;
        } else {
            this.clearError(email);
        }

        // Password validation
        if (password.value.length < 6) {
            this.showError(password, 'Password must be at least 6 characters long');
            isValid = false;
        } else {
            this.clearError(password);
        }

        // Confirm password validation
        if (password.value !== confirmPassword.value) {
            this.showError(confirmPassword, 'Passwords do not match');
            isValid = false;
        } else {
            this.clearError(confirmPassword);
        }

        if (!isValid) {
            e.preventDefault();
        }
    }

    validateLoginForm(e) {
        const form = e.target;
        const email = form.querySelector('#email');
        const password = form.querySelector('#password');

        let isValid = true;

        if (!this.isValidEmail(email.value)) {
            this.showError(email, 'Please enter a valid email address');
            isValid = false;
        } else {
            this.clearError(email);
        }

        if (password.value.length === 0) {
            this.showError(password, 'Please enter your password');
            isValid = false;
        } else {
            this.clearError(password);
        }

        if (!isValid) {
            e.preventDefault();
        }
    }

    validateResumeForm(e) {
        const form = e.target;
        const title = form.querySelector('#title');
        const educationEntries = form.querySelectorAll('[name*="education"][name*="institution"]');
        const experienceEntries = form.querySelectorAll('[name*="experience"][name*="company"]');

        let isValid = true;

        // Title validation
        if (title.value.trim().length === 0) {
            this.showError(title, 'Resume title is required');
            isValid = false;
        } else {
            this.clearError(title);
        }

        // Education validation
        educationEntries.forEach((input, index) => {
            if (input.value.trim().length === 0) {
                this.showError(input, 'Institution name is required');
                isValid = false;
            } else {
                this.clearError(input);
            }
        });

        // Experience validation
        experienceEntries.forEach((input, index) => {
            if (input.value.trim().length === 0) {
                this.showError(input, 'Company name is required');
                isValid = false;
            } else {
                this.clearError(input);
            }
        });

        if (!isValid) {
            e.preventDefault();
            this.scrollToFirstError();
        }
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    showError(input, message) {
        this.clearError(input);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.style.color = '#f56565';
        errorDiv.style.fontSize = '0.8rem';
        errorDiv.style.marginTop = '0.25rem';
        errorDiv.textContent = message;
        
        input.style.borderColor = '#f56565';
        input.parentNode.appendChild(errorDiv);
    }

    clearError(input) {
        const existingError = input.parentNode.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }
        input.style.borderColor = '';
    }

    scrollToFirstError() {
        const firstError = document.querySelector('.form-error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Dynamic Form Management
class DynamicFormManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindDynamicEvents();
    }

    bindDynamicEvents() {
        // Skills input enhancement
        const skillsInput = document.getElementById('skills');
        if (skillsInput) {
            skillsInput.addEventListener('keydown', (e) => this.handleSkillsInput(e));
        }

        // Awards input enhancement
        const awardsInput = document.getElementById('awards');
        if (awardsInput) {
            awardsInput.addEventListener('keydown', (e) => this.handleAwardsInput(e));
        }
    }

    handleSkillsInput(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.addSkillFromInput(e.target);
        }
    }

    handleAwardsInput(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.addAwardFromInput(e.target);
        }
    }

    addSkillFromInput(input) {
        const value = input.value.trim();
        if (value && !value.endsWith(',')) {
            input.value = value + ', ';
        }
    }

    addAwardFromInput(input) {
        const value = input.value.trim();
        if (value && !value.endsWith(',')) {
            input.value = value + ', ';
        }
    }
}

// Dashboard Interactivity
class DashboardManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindDashboardEvents();
        this.initCharts();
    }

    bindDashboardEvents() {
        // Search functionality
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e));
        }

        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e));
        });
    }

    handleSearch(e) {
        const searchTerm = e.target.value.toLowerCase();
        const resumeCards = document.querySelectorAll('.resume-card');
        
        resumeCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            if (title.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    handleFilter(e) {
        const filter = e.target.dataset.filter;
        // Implement filter logic based on your needs
        console.log('Filter by:', filter);
    }

    initCharts() {
        // Initialize any charts for admin dashboard
        if (typeof Chart !== 'undefined' && document.getElementById('statsChart')) {
            this.initStatsChart();
        }
    }

    initStatsChart() {
        // Example chart implementation
        const ctx = document.getElementById('statsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Resumes Created',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: '#667eea',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
}

// Notification System
class NotificationSystem {
    constructor() {
        this.init();
    }

    init() {
        this.bindNotificationEvents();
    }

    bindNotificationEvents() {
        // Auto-hide alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                this.fadeOut(alert);
            }, 5000);
        });
    }

    fadeOut(element) {
        element.style.transition = 'opacity 0.5s ease';
        element.style.opacity = '0';
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 500);
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} glass`;
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '10000';
        notification.style.maxWidth = '300px';

        document.body.appendChild(notification);

        setTimeout(() => {
            this.fadeOut(notification);
        }, 5000);
    }
}

// Main Application
class ResumeGeneratorApp {
    constructor() {
        this.themeManager = new ThemeManager();
        this.formValidator = new FormValidator();
        this.dynamicFormManager = new DynamicFormManager();
        this.dashboardManager = new DashboardManager();
        this.notificationSystem = new NotificationSystem();
        this.init();
    }

    init() {
        this.bindGlobalEvents();
        this.enhanceUX();
    }

    bindGlobalEvents() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Smooth scrolling for anchor links
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                const target = document.querySelector(e.target.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    }

    handleKeyboardShortcuts(e) {
        // Toggle theme with Ctrl/Cmd + T
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
            e.preventDefault();
            this.themeManager.toggleTheme();
        }

        // Focus search with Ctrl/Cmd + K
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
    }

    enhanceUX() {
        // Add loading states to buttons
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                    submitBtn.disabled = true;
                }
            });
        });

        // Add hover effects to interactive elements
        const interactiveElements = document.querySelectorAll('.btn, .card, .nav-link');
        interactiveElements.forEach(el => {
            el.style.transition = 'all 0.3s ease';
        });

        // Lazy loading for images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ResumeGeneratorApp();
});

// Utility functions
const utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    },

    generatePDFPreview(resumeData) {
        // This would generate a visual preview of the PDF
        console.log('Generating PDF preview for:', resumeData);
    }
};

// Export for global access if needed
window.ResumeGeneratorApp = ResumeGeneratorApp;
window.utils = utils;
