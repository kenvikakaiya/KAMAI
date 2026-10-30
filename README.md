# KAMAI – Micro-Earning Platform

## Project Overview

KAMAI is a web-based micro-earning platform that allows users to discover available tasks, accept work, submit completed tasks, and earn rewards.

It also provides an admin panel to review submissions, approve or reject work, and manage reward payments.

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
├── instance/          # Runtime application data
│
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

### 1. Clone the Repository

```bash
git clone https://github.com/kenvikakaiya/KAMAI.git
cd KAMAI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file by copying `.env.example`.

For Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open the `.env` file and configure your environment variables.

Example:

```env
SECRET_KEY=your_generated_secret_key
DATABASE_URL=sqlite:///kamai.db
```

Generate your own secure secret key and use the database configuration appropriate for your setup.

**Important:** Never upload your `.env` file, secret keys, passwords, or private credentials to GitHub.

### 6. Run the Application

```bash
python app.py
```

Open the local address displayed in the terminal in your web browser.

## Security Measures

- Passwords are stored using secure password hashing.
- Login-required routes protect user-specific features.
- Role-based checks restrict admin functionality.
- CSRF protection is enabled for form submissions.
- Database transactions and rollback handling protect important updates.
- Task and submission statuses control the earning workflow.
- Environment variables are used to manage sensitive configuration.
- Git ignore rules help prevent sensitive environment files from being committed.

## Project Purpose

This project was developed to practice full-stack web development, database management, authentication, access control, backend development, and real-world workflow implementation using Flask.

## Developer

**Kenvi Kakaiya**

MCA Student | Aspiring Software Developer

- GitHub: [kenvikakaiya](https://github.com/kenvikakaiya)
- Project Repository: [KAMAI – Micro-Earning Platform](https://github.com/kenvikakaiya/KAMAI)