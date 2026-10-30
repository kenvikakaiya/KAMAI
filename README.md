# KAMAI – Micro-Earning Platform

## Project Overview

KAMAI is a web-based micro-earning platform that allows users to discover available tasks, accept work, submit completed tasks, and earn rewards. It also provides an admin panel to review submissions, approve or reject work, and manage reward payments.

The platform is designed to provide a simple and organized task-based earning workflow.

## Key Features

- **User Authentication:** User registration and login.
- **Task Management:** Browse available tasks and view task details.
- **Task Acceptance:** Accept tasks before starting work.
- **Work Submission:** Submit completed work for admin review.
- **Admin Panel:** Review, approve, and reject submissions.
- **Wallet Management:** Track available and pending balances.
- **Transaction History:** View recorded earning transactions.
- **Access Control:** Separate permissions for administrators and earners.
- **Security:** Password hashing, login protection, and CSRF protection.

## Technology Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (default configuration) |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Form Security | Flask-WTF, CSRF Protection |
| Environment Configuration | python-dotenv |
| Version Control | Git, GitHub |
| Development Tool | Visual Studio Code |

## Project Workflow

1. User registers or logs in.
2. User explores available tasks.
3. User accepts a task.
4. User completes and submits the work.
5. Admin reviews the submission.
6. Admin approves or rejects the work.
7. When approved, the reward is credited to the user's wallet.
8. User checks wallet balance and transaction history.

## Project Structure

```text
KAMAI/
│
├── models/
│   ├── user.py
│   ├── task.py
│   ├── submission.py
│   ├── wallet.py
│   └── service.py
│
├── routes/
│   ├── auth.py
│   ├── tasks.py
│   ├── submissions.py
│   ├── admin.py
│   ├── wallet.py
│   └── my_work.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── instance/
├── app.py
├── config.py
├── extensions.py
├── create_admin.py
├── seed_tasks.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd KAMAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure:

```env
SECRET_KEY=your_generated_secret_key
DATABASE_URL=sqlite:///kamai.db
```

Use your own secure secret key. Never upload the `.env` file to GitHub.

### 6. Run the application

```bash
python app.py
```

Open the local address displayed by Flask in your browser.

## Security Measures

- Passwords are stored using secure password hashing.
- Login-required routes protect user-specific features.
- Role-based checks restrict admin functionality.
- CSRF protection is enabled for form submissions.
- Database transactions and rollback handling protect important updates.
- Task and submission statuses control the earning workflow.

## Project Purpose

This project was developed to practice full-stack web development, database management, authentication, access control, backend development, and real-world workflow implementation using Flask.

## Developer

**Kenvi Kakaiya**

MCA Student | Aspiring Software Developer

