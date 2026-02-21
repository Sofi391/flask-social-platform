# 📝 Flask Social Platform

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green)](https://flask.palletsprojects.com/)  
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red)](https://www.sqlalchemy.org/)  
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)](https://getbootstrap.com/)  
[![License](https://img.shields.io/badge/License-MIT-yellow)](#)

A **full-stack Flask application** designed as a social blogging platform where users can create, share, and engage with content. This project highlights foundational **backend development skills** including authentication, role-based permissions, relational database design, and notification systems.

> 📸 **Screenshots**: Check out the [screenshots gallery](screenshots/GALLERY.md) to see every page and feature in action.

---

## ✨ Project Overview

Flask Social Platform simulates a **real-world social media/blogging environment**, allowing users to:

- Publish posts and rich-formatted content
- Engage with posts through comments and likes
- Receive in-app and email notifications for interactions
- Manage profiles and personal content
- Experience role-based access (User, Admin, Super Admin)

The platform emphasizes **backend concepts** such as secure authentication, relational data management, query optimization, and filtering.

Admins can moderate content, manage users, and ensure platform quality. The project demonstrates **production-ready practices**, though it is primarily educational to showcase backend growth and framework versatility.

---

## 🛠 Core Features

### 🔐 Authentication & User Management
- Secure registration and login with password hashing (PBKDF2-SHA256)
- Email-based password reset with verification
- Profile management with Gravatar integration
- Role-based permissions (User, Admin, Super Admin)

### 📝 Content Management
- Rich-text blog posts with CKEditor
- Create, edit, delete posts
- Image support via URLs
- Post search by title or author
- Dynamic feed with custom refresh

### 💬 Social Interactions
- Nested comments with edit/delete
- Like system for posts and comments
- In-app notifications for interactions
- Email notifications for important account activities

### 🛡 Admin Dashboard
- User management: promote, demote, restrict, or remove
- Content moderation: delete posts/comments
- Role hierarchy: Super Admin overrides Admin privileges

### ⚙️ Backend Concepts
- Relational database management with SQLAlchemy (SQLite)
- Filtering and query optimization
- Environment-based configuration using `.env`
- Security: CSRF protection, session management, input validation

---

## ⚙️ Tech Stack

- **Backend:** Flask 2.3.2  
- **Database:** SQLite with SQLAlchemy 2.0.25  
- **Authentication:** Flask-Login 0.6.3  
- **Forms:** Flask-WTF 1.2.1 + WTForms 3.0.1  
- **UI Framework:** Bootstrap 5 (Bootstrap-Flask 2.2.0)  
- **Rich Text:** Flask-CKEditor 0.4.6  
- **Email:** SMTP with Gmail integration  
- **Security:** PBKDF2-SHA256 hashing, CSRF protection  
- **Environment:** python-dotenv 1.0.0  

---

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd flask_socials
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///posts.db
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

5. **Run the application**
```bash
python main.py
```

The application will be available at `http://localhost:5000`

---

## ⚙️ Configuration

### Email Setup
For Gmail SMTP:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: Google Account → Security → App Passwords
3. Use the generated password in `EMAIL_PASSWORD`

### Database
The application uses SQLite by default. The database is automatically created on first run.

---

## 🧱 Project Structure

```
flask_socials/
├── static/
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── assets/       # Images and icons
├── templates/        # HTML templates
├── instance/         # Database files
├── main.py          # Application entry point
├── models.py        # Database models
├── forms.py         # WTForms definitions
├── database.py      # Database configuration
├── requirements.txt # Python dependencies
├── .env            # Environment variables (not in git)
├── .env.example    # Environment template
└── .gitignore      # Git ignore rules
```

Modular structure improves maintainability, scalability, and clarity.

---

## 🌐 Application Overview

The app provides a REST-like interface:

- **Public pages**: home feed, about, contact, post views, search  
- **Authenticated routes**: create/edit/delete posts, like/unlike, comments, notifications  
- **Admin routes**: user promotion/demotion, restriction, deletion, content moderation

---

## 🛡 Production Practices

- Environment-based configuration  
- Secure authentication and password hashing  
- Role-based access control  
- CSRF protection and session management  
- Input validation and sanitization  
- Relational database with SQLAlchemy ORM
- Query filtering and optimization  
- Email notifications for key events  

---

## 🎯 Learning Outcomes

- Full-stack application design using Flask  
- Secure authentication & role-based permissions  
- Relational database modeling  
- Real-time notification systems  
- Rich text editing integration  
- Managing backend workflows and security  
- Growth story: first major backend project showcasing foundational skills  

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 About the Developer

Hi! I’m **Sofi (Sofoniyas)** — a **Backend Developer** and **Software Engineering student at AASTU**, graduate of the **ALX Backend Engineering Program**.  

I build **secure, scalable, and production-ready backend applications**. 
This project shows my **first hands-on experience with Flask**, demonstrating my growth to more complex Django and API projects.

---

### 🤝 Connect with Me

<p align="center">
  <a href="https://linkedin.com/in/sofoniyas-alebachew-bb876b33b">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/Sofi391">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
</p>

---

## 📄 License

This project is open source and available under the MIT License.

--- 

**⭐ If you find this project helpful, please consider giving it a star!**