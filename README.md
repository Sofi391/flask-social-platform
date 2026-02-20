# 📝 Flask Socials

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green)](https://flask.palletsprojects.com/)  
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red)](https://www.sqlalchemy.org/)  
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)](https://getbootstrap.com/)  
[![License](https://img.shields.io/badge/License-MIT-yellow)](#)

A production-ready **full-stack blog platform** built with Flask that enables users to create, share, and engage with content through posts, comments, and social interactions.

This platform provides a complete blogging experience with user authentication, rich text editing, social features, real-time notifications, and a powerful admin dashboard for content moderation and user management.

---

## ✨ Project Overview

Flask Socials is designed to simulate a real-world social blogging platform where users can:

- Create and publish rich-formatted blog posts
- Engage with content through comments and likes
- Receive real-time notifications for interactions
- Manage their profile and content
- Experience role-based access control

Admins have powerful tools to moderate content, manage users, and maintain platform quality. The project demonstrates production-grade practices including secure authentication, email integration, and environment-based configuration.

> 📸 **Check out the `/screenshots` folder to see the web interface and application features in action!**

---

## 🛠 Core Features

### 🔐 Authentication & User Management
- **Authentication System**: Secure user registration and login with password hashing
- **Password Recovery**: Email-based password reset with time-limited verification codes
- **User Profiles**: Personalized profiles with Gravatar integration
- **Role-Based Access Control**: Multi-tier permission system (User, Admin, Super Admin)

---

### 📝 Content Management
- **Rich Text Editor**: CKEditor integration for creating formatted blog posts
- **Post Operations**: Create, edit, delete, and view blog posts
- **Image Support**: Add custom images to posts via URL
- **Search Functionality**: Search posts by title and author name
- **Dynamic Feed**: Randomized post display with infinite scroll loading

---

### 💬 Social Features
- **Comments System**: Nested commenting with edit and delete capabilities
- **Like System**: Like posts and comments with real-time updates
- **Notifications**: In-app notification system for user interactions
- **Email Notifications**: Automated email alerts for important account activities

---

### 🛡 Admin Dashboard
- **User Management**: Promote, demote, restrict, or remove users
- **Content Moderation**: Admin and post author can delete comments
- **Access Control**: Restrict users from posting and commenting
- **Role Hierarchy**: Super Admin has elevated privileges over regular admins

---

## ⚙️ Tech Stack

- **Backend**: Flask 2.3.2
- **Database**: SQLAlchemy 2.0.25 with SQLite
- **Authentication**: Flask-Login 0.6.3
- **Forms**: Flask-WTF 1.2.1 with WTForms 3.0.1
- **UI Framework**: Bootstrap 5 (Bootstrap-Flask 2.2.0)
- **Rich Text**: Flask-CKEditor 0.4.6
- **Email**: SMTP with Gmail integration
- **Security**: Werkzeug 3.0.0 for password hashing
- **Environment**: python-dotenv 1.0.0

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

---

## 💾 Database Models

- **User**: User accounts with authentication and role management
- **BlogPost**: Blog posts with title, content, images, and metadata
- **Comments**: User comments on posts with edit tracking
- **Likes**: Like relationships for posts and comments
- **Notifications**: In-app notification system

---

## 🔒 Security Features

- Password hashing with PBKDF2-SHA256
- CSRF protection on all forms
- Session management with secure cookies
- Environment-based configuration
- SQL injection prevention via SQLAlchemy ORM
- Role-based access control decorators

---

## 🌐 Application Routes

### Public Routes
- `GET /` - Home page with blog feed
- `GET /about` - About page
- `GET /contact` - Contact form
- `GET /post/<id>` - View individual post
- `GET /search` - Search posts

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET/POST /forget_password` - Password reset request
- `GET/POST /verification` - Verify reset code
- `GET/POST /password_reset` - Reset password

### User Routes (Login Required)
- `GET /my_posts/<user_id>` - User's posts
- `GET/POST /new_post` - Create new post
- `GET/POST /edit/<id>` - Edit post
- `GET /delete/<id>` - Delete post
- `POST /post_like/<post_id>` - Like/unlike post
- `POST /like_comment/<comment_id>` - Like/unlike comment
- `GET /notifications` - View notifications

### Admin Routes
- `GET /admin_dashboard` - Admin control panel
- `GET /promote/<user_id>` - Promote user to admin
- `GET /demote/<user_id>` - Demote admin to user
- `GET /restrict_user/<user_id>` - Restrict user access
- `GET /unrestrict_user/<user_id>` - Remove restrictions
- `GET /remove_user/<user_id>` - Delete user account

---

## 🛡 Production-Ready Practices

- Environment-based configuration using `.env`
- Secure password hashing with PBKDF2-SHA256
- CSRF protection on all forms
- SQL injection prevention via SQLAlchemy ORM
- Role-based access control system
- Email notification system for user activities
- Session management with secure cookies
- Gravatar integration for user avatars
- Input validation and sanitization

---

## 🎯 Learning Outcomes

- Building full-stack web applications with Flask
- Implementing secure authentication and authorization systems
- Designing relational database schemas with SQLAlchemy
- Creating role-based permission systems
- Integrating rich text editors (CKEditor)
- Building real-time notification systems
- Implementing email functionality with SMTP
- Managing user sessions and cookies
- Writing production-ready Flask applications
- Following security best practices

---

## 👨‍💻 About the Developer

Hi! I'm **Sofi (Sofoniyas)** — a **Full-Stack Developer** and **Software Engineering student at AASTU**, and a **graduate of the ALX Backend Engineering Program**.

I specialize in building **secure, scalable, and production-ready web applications** using modern technologies. I enjoy translating real-world requirements into clean, maintainable, and efficient solutions.

I'm particularly interested in:

- Full-stack web development with Flask and Django
- Authentication, authorization, and security best practices
- Building scalable backend systems and RESTful APIs
- Database design and optimization
- Creating intuitive user experiences
- Writing clean, maintainable code

This project showcases my ability to build complete web applications with complex features like social interactions, notifications, and admin dashboards while following production-grade practices.

---

### 🤝 Connect with Me

[<img align="left" alt="LinkedIn" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />][linkedin]  
[<img align="left" alt="GitHub" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/github.svg" />][github]  

[linkedin]: https://linkedin.com/in/sofoniyas-alebachew-bb876b33b
[github]: https://github.com/sofi391

<br />

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 💬 Support

For issues, questions, or contributions, please use the contact form or open an issue on the repository.

---

**⭐ If you find this project helpful, please consider giving it a star!**
