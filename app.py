import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_generator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resumes = db.relationship('Resume', backref='author', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    education = db.Column(db.JSON)
    experience = db.Column(db.JSON)
    skills = db.Column(db.JSON)
    awards = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('signup'))
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# User Dashboard Routes
@app.route('/dashboard')
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', resumes=resumes)

@app.route('/create_resume', methods=['GET', 'POST'])
@login_required
def create_resume():
    if request.method == 'POST':
        # Parse form data
        education = []
        experience = []
        skills = []
        awards = []
        
        # Parse education entries
        i = 0
        while f'education[{i}][institution]' in request.form:
            education.append({
                'institution': request.form.get(f'education[{i}][institution]'),
                'degree': request.form.get(f'education[{i}][degree]'),
                'field': request.form.get(f'education[{i}][field]'),
                'start_date': request.form.get(f'education[{i}][start_date]'),
                'end_date': request.form.get(f'education[{i}][end_date]'),
                'description': request.form.get(f'education[{i}][description]')
            })
            i += 1
        
        # Parse experience entries
        i = 0
        while f'experience[{i}][company]' in request.form:
            experience.append({
                'company': request.form.get(f'experience[{i}][company]'),
                'position': request.form.get(f'experience[{i}][position]'),
                'start_date': request.form.get(f'experience[{i}][start_date]'),
                'end_date': request.form.get(f'experience[{i}][end_date]'),
                'description': request.form.get(f'experience[{i}][description]')
            })
            i += 1
        
        # Parse skills and awards
        skills_text = request.form.get('skills', '')
        awards_text = request.form.get('awards', '')
        
        skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        awards = [a.strip() for a in awards_text.split(',') if a.strip()]
        
        resume = Resume(
            title=request.form.get('title'),
            summary=request.form.get('summary'),
            education=education,
            experience=experience,
            skills=skills,
            awards=awards,
            user_id=current_user.id
        )
        
        db.session.add(resume)
        db.session.commit()
        
        flash('Resume created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_resume.html')

@app.route('/edit_resume/<int:resume_id>', methods=['GET', 'POST'])
@login_required
def edit_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if user owns the resume or is admin
    if resume.user_id != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to edit this resume!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Parse form data
        education = []
        experience = []
        skills = []
        awards = []
        
        # Parse education entries
        i = 0
        while f'education[{i}][institution]' in request.form:
            education.append({
                'institution': request.form.get(f'education[{i}][institution]'),
                'degree': request.form.get(f'education[{i}][degree]'),
                'field': request.form.get(f'education[{i}][field]'),
                'start_date': request.form.get(f'education[{i}][start_date]'),
                'end_date': request.form.get(f'education[{i}][end_date]'),
                'description': request.form.get(f'education[{i}][description]')
            })
            i += 1
        
        # Parse experience entries
        i = 0
        while f'experience[{i}][company]' in request.form:
            experience.append({
                'company': request.form.get(f'experience[{i}][company]'),
                'position': request.form.get(f'experience[{i}][position]'),
                'start_date': request.form.get(f'experience[{i}][start_date]'),
                'end_date': request.form.get(f'experience[{i}][end_date]'),
                'description': request.form.get(f'experience[{i}][description]')
            })
            i += 1
        
        # Parse skills and awards
        skills_text = request.form.get('skills', '')
        awards_text = request.form.get('awards', '')
        
        skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        awards = [a.strip() for a in awards_text.split(',') if a.strip()]
        
        resume.title = request.form.get('title')
        resume.summary = request.form.get('summary')
        resume.education = education
        resume.experience = experience
        resume.skills = skills
        resume.awards = awards
        resume.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Resume updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_resume.html', resume=resume)

@app.route('/delete_resume/<int:resume_id>')
@login_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if user owns the resume or is admin
    if resume.user_id != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this resume!', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# PDF Generation
@app.route('/download_resume/<int:resume_id>')
@login_required
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if user owns the resume or is admin
    if resume.user_id != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to download this resume!', 'error')
        return redirect(url_for('dashboard'))
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    story = []
    
    # Title
    story.append(Paragraph(resume.title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    if resume.summary:
        story.append(Paragraph("SUMMARY", heading_style))
        story.append(Paragraph(resume.summary, normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Education
    if resume.education:
        story.append(Paragraph("EDUCATION", heading_style))
        for edu in resume.education:
            edu_text = f"<b>{edu.get('degree', '')} in {edu.get('field', '')}</b><br/>"
            edu_text += f"{edu.get('institution', '')}<br/>"
            edu_text += f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
            if edu.get('description'):
                edu_text += f"<br/>{edu.get('description')}"
            story.append(Paragraph(edu_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Experience
    if resume.experience:
        story.append(Paragraph("EXPERIENCE", heading_style))
        for exp in resume.experience:
            exp_text = f"<b>{exp.get('position', '')}</b> at {exp.get('company', '')}<br/>"
            exp_text += f"{exp.get('start_date', '')} - {exp.get('end_date', '')}"
            if exp.get('description'):
                exp_text += f"<br/>{exp.get('description')}"
            story.append(Paragraph(exp_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Skills
    if resume.skills:
        story.append(Paragraph("SKILLS", heading_style))
        skills_text = ", ".join(resume.skills)
        story.append(Paragraph(skills_text, normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Awards
    if resume.awards:
        story.append(Paragraph("AWARDS & CERTIFICATIONS", heading_style))
        for award in resume.awards:
            story.append(Paragraph(f"• {award}", normal_style))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{resume.title.replace(' ', '_')}.pdf",
        mimetype='application/pdf'
    )

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_resumes=total_resumes,
                         recent_users=recent_users)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/resumes')
@login_required
def admin_resumes():
    if current_user.role != 'admin':
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    resumes = Resume.query.all()
    return render_template('admin_resumes.html', resumes=resumes)

# API Routes for statistics
@app.route('/api/stats')
@login_required
def api_stats():
    if current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'total_resumes': Resume.query.count(),
        'users_today': User.query.filter(
            User.created_at >= datetime.today().date()
        ).count()
    }
    
    return jsonify(stats)

def init_db():
    """Initialize the database and create default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            
        # Create sample regular user
        sample_user = User.query.filter_by(email='user@example.com').first()
        if not sample_user:
            sample_user = User(
                email='user@example.com',
                password_hash=generate_password_hash('user123'),
                role='user'
            )
            db.session.add(sample_user)
            
        db.session.commit()
        print("✓ Database initialized successfully!")
        print("✓ Default users created:")
        print("  Admin: admin@example.com / admin123")
        print("  User:  user@example.com / user123")

if __name__ == '__main__':
    print("Starting Resume Generator Application...")
    init_db()
    print("🚀 Application running at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
