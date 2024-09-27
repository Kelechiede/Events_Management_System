# Events Management System

## Project Description

This is an Events Management System built with Flask. The system allows users to sign up, log in, create, update, delete, and view events. It also includes data visualizations for event statistics.

## Features

- User Authentication (Sign Up, Log In, Log Out)
- Create, Update, and Delete Events
- Manage Venues
- View and Register for Events
- Data Visualizations (Event Popularity, User Registration Trends, etc.)

## Project Structure

```bash
Events_Management_System/
├── app.py
├── models.py
├── requirements.txt
├── Procfile
├── data_ingestion.py                  # Script for data ingestion
├── clear_data.py                      # Script to clear existing data
├── notebooks/event_analysis.ipynb  # run on jupyter notebook IDE
├── scripts/
│   ├── data_ingestion.py              # Optional: Can also be placed here
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── users.html
│   ├── add_user.html
│   ├── update_user.html
│   ├── venues.html
│   ├── add_venue.html
│   ├── update_venue.html
│   ├── events.html
│   ├── add_event.html
│   ├── update_event.html
│   ├── visualizations.html
│   ├── csrf_error.html
│   ├── login.html
│   ├── signup.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│       └── script.js
├── environ/
│   ├── Scripts/
│   │   ├── activate
│   │   ├── ...
│   ├── ...
└── ...


Installation
1. Clone the repository: 
git clone https://github.com/Kelechiede/Events_Management_System.git
cd Events_Management_System 

2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
pip install -r requirements.txt

4. Set up the database:
flask db init
flask db migrate
flask db upgrade

5. Populate the database with sample data:
python scripts/data_ingestion.py

6. Run the application:
flask run

Usage
Navigate to http://127.0.0.1:5000 in your web browser to access the application.
Sign up for a new account or log in with an existing account.
Explore the features such as managing events, venues, and viewing data visualizations.

**Live Demo**

Check out the live demo of the Events Management System: [Live Demo](https://events-management-system-890b21f6a4d2.herokuapp.com/)


License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Kelechukwu Innocent Ede
