# ResumeGen - Professional Resume Generator
![ResumeGen](https://img.shields.io/badge/ResumeGen-Professional-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-green) ![Python](https://img.shields.io/badge/Python-3.8%252B-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

A modern, full-stack web application for creating professional resumes and CVs with instant PDF download capability. Features a stunning glassmorphism design with dark/light mode toggle.

---

## 🚀 Features

### ✨ Core Functionality
- **User Authentication** - Secure signup/login with session management  
- **Resume Management** - Create, edit, delete, and view multiple resumes  
- **PDF Generation** - Instant professional PDF downloads using ReportLab  
- **Dynamic Forms** - Add multiple education and experience entries  
- **Skills & Awards** - Easy comma-separated input for quick entry  

### 🎨 User Experience
- **Glassmorphism Design** - Modern, futuristic UI with transparency effects  
- **Dark/Light Mode** - Toggle between themes with persistent preferences  
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile  
- **Form Validation** - Client-side and server-side validation  
- **Real-time Previews** - Dynamic form updates with instant feedback  

### 👑 Admin Features
- **User Management** - View and manage all registered users  
- **Resume Oversight** - Access and manage all resumes in the system  
- **Dashboard Analytics** - Platform statistics and usage metrics  
- **Role-based Access** - Secure admin-only functionality  

---

## 🛠 Tech Stack

### Backend
- Flask - Python web framework  
- SQLAlchemy - ORM for database operations  
- Flask-Login - Session-based authentication  
- ReportLab - PDF generation and formatting  
- Werkzeug - Password hashing and security  

### Frontend
- HTML5 - Semantic markup  
- CSS3 - Glassmorphism design with CSS variables  
- JavaScript - Dynamic form handling and theme management  
- Font Awesome - Modern icon library  

### Database
- SQLite - Development (default)  
- PostgreSQL - Production ready  

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher  
- pip (Python package manager)  

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/resume-generator.git
cd resume-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```
### Access the application
  http://localhost:5000

### Default Login Credentials

  **Admin Account**: admin@example.com
                / admin123

  **User Account**: user@example.com
               / user123

---

## 🗄 Database Setup
### SQLite (Default - Development)

- The application uses SQLite by default. No additional setup required.

#### PostgreSQL (Production)
```
CREATE DATABASE resume_generator;
CREATE USER resume_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_generator TO resume_user;
```

- Update database configuration in app.py:
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://resume_user:your_password@localhost/resume_generator'
```
---
## 📁 Project Structure
```
resume_generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   ├── dashboard.html    # User dashboard
│   ├── create_resume.html # Resume creation form
│   ├── edit_resume.html  # Resume editing form
│   ├── admin_dashboard.html # Admin overview
│   ├── admin_users.html  # User management
│   └── admin_resumes.html # Resume management
└── static/
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── script.js     # Main JavaScript file
```
---
## 🎯 Usage
### For Users

- Sign Up - Create a new account

- Login - Access your personal dashboard

- Create Resume - Fill in professional details using dynamic forms

- Manage Resumes - Edit, update, or delete existing resumes

- Download PDF - Generate and download professionally formatted resumes

### For Admins

- Access Admin Panel - Navigate to /admin

- View Statistics - Monitor platform usage and metrics

- Manage Users - Oversee all registered users

- Manage Resumes - Access and manage all resumes in the system

---

## 🔧 API Endpoints
```
Method	          Endpoint	            Description	              Access
GET	                 /	                 Homepage	                Public
GET/POST	         /signup	          User registration	          Public
GET/POST	         /login	          User authentication	          Public
GET	              /logout	              User logout	              Authenticated
GET	             /dashboard	          User dashboard	            Authenticated
GET/POST	      /create_resume	      Create new resume	          Authenticated
GET/POST	    /edit_resume/<id>	      Edit existing resume      	Owner/Admin
GET	          /delete_resume/<id>	       Delete resume	          Owner/Admin
GET	         /download_resume/<id>	      Download PDF	          Owner/Admin
GET	              /admin	              Admin dashboard	          Admin only
GET	            /admin/users	          User management	          Admin only
GET	          /admin/resumes	        Resume management	          Admin only
```
---
<div align="center"> Made with ❤️ by [Your Name]

⭐ Star this repo on GitHub

</div>
---
## 🔮 Future Enhancements

- **AI-Powered Suggestions** - Smart content recommendations

- **Multiple Templates** - Choose from different resume designs

- **Cover Letter Generator** - Generate matching cover letters

- **Job Search Integration** - Connect with job boards

- **Resume Analytics** - Track views and downloads

- **Multi-language Support** - Internationalization

- **Cloud Storage** - Sync across devices

- **Mobile App** - Native iOS/Android applications

---

## 📊 Performance Metrics

- **Page Load Time**: < 2 seconds

- **PDF Generation**: < 3 seconds

- **Database Queries**: Optimized with SQLAlchemy

- **Mobile Performance**: Fully responsive design

---

## 🔒 Security Features

- Password hashing with Werkzeug

- Session-based authentication

- CSRF protection

- SQL injection prevention

- XSS protection

- Secure file upload handling
