# 🧾 Pensions Web Integration (Django)

A web application built with Django that connects to an SQL database for managing pension-related records.  
It provides a simple and user-friendly interface for viewing, updating, and maintaining pension data.

---

## 🚀 Features

- 📄 View and manage pensioner records
- 📝 Add, update, or delete pension entries
- 🔍 Search functionality
- 📊 Basic dashboard (optional for analytics)
- 🔐 Authentication 

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap, JavaScript
- **Database**: SQL Server / PostgreSQL / MySQL 

---

---

## ⚙️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/maingijustoo/pensions-web.git
   cd pensions-web


2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
create and activate virtual environment



1. **create and activate virtual environment**

   ```bash
   pip install -r requirements.txt
   
Configure your database in settings.py



Update the DATABASES section with your SQL database connection details.


1. **Apply migrations and run server**

   ```bash

   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver


📄 License
MIT License. Free to use, modify, and share.

🙏 Acknowledgements
Built as a practical system to streamline pension record management using Django and SQL integration.
