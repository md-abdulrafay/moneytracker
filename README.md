# Truly Expenses - Personal Finance Management System

## Overview
Truly Expenses is a personal finance management system built with Django. It helps users track their income, expenses, and transfers efficiently. The system allows users to manage their finances with ease, providing a simple yet powerful tool to monitor financial activity.

## Features
- **Budget Management**: Set monthly or category-based budgets, receive alerts when exceeding limits, and track financial discipline.
- **User Authentication**: Secure login and registration system.
- **Expense Tracking**: Add, edit, delete, and categorize expenses.
- **Income Management**: Record income sources and transactions.
- **Transfers**: Track money transfers between different accounts.
- **User Preferences**: Customize settings such as currency preferences.
- **Reports and Insights**: View summaries of income and expenses for better financial analysis.
- **Responsive UI**: Designed for both desktop and mobile use.

## Installation

### Prerequisites
- Python 3.8+
- Django 4+
- Pipenv
- PostgreSQL

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/truly-expenses.git
   cd truly-expenses
   ```
2. Install dependencies using Pipenv:
   ```sh
   pipenv install --dev
   ```
3. Activate the virtual environment:
   ```sh
   pipenv shell
   ```
4. Configure the PostgreSQL database:
   - Create a PostgreSQL database and user.
   - Update `settings.py` with database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser (for admin access):
   ```sh
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```sh
   python manage.py runserver
   ```
8. Open the app in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Usage
- Sign up and log in to manage your personal finances.
- Add income and expenses with categories.
- View reports and track financial trends.
- Update user preferences such as currency settings.

## Contributing
Contributions are welcome! If you'd like to improve the project, feel free to submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or issues, please reach out to [abdulrafay.2dec@gmail.com].

