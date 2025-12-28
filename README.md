# VERY VEGGIE TRACKER
#### Video Demo: <URL HERE>
#### Description: A specialized web application for tracking the 10-generation Sims 4 "Very Veggie Legacy Challenge" by lilsimsie.
## The Very Veggie Legacy Tracker

The Sims 4 is a social simulation game developed by Maxis and published by Electronic Arts. The Very Veggie Legacy Challenge is a ruleset for The Sims 4, created by [lilsimsie](https://www.youtube.com/lilsimsie), a popular Sims 4 YouTuber. Historically, players have tracked their progress in legacy challenges using complex spreadsheets or paper notes. This project provides a dynamic, web-based alternative that automates goal tracking, visualizes progress with them-accurate colors, and persists data across user sessions.

### Project Motivation

### Features
* **Interactive Dashboard:** Dynamic progress bars that update as you complete goals.
* **Full-Stack Interactivity:** Uses JavaScript `Fetch API` to update the database without page reloads.
* **Sims Aesthetic:** Clean UI built with W3.CSS, featuring custom 3D-style vegetable icons.
* **Secure Auth:** Session-based login and registration with inline error handling.

### Technology Stack
* **Backend:** Python/Flask
* **Database:** SQLite3
* **Frontend:** Jinja2 Templates, W3.CSS, Vanill JavaScript
* **Assets:** Custom AI-generated 3D Vegetable Graphics

### How It Works
1. A user starts with the login page. 
   * If they have an account, they can login with their username and password.
   * If the user does not have an account they may select **Register** from the main menu to open the registration page and create a username and password. Duplicate usernames are not allowed. 
   * Once they have created an account, they will be returned to the login page to enter the site.
2. Once users are logged in, they see their **Dashboard** where there is a card for each of the generations of the legacy challenge. On each card is a progress bar that indicates their percentage of completion of the requirements for that generation.
3. If a user clicks clicks on a card, they are taken to generation subpage where there is a list of requirements for the generation. Users then click the checkbox as they complete each requirement. When the user returns to the **Dashboard**, the progress bar for that generation has been updated.
4. The user can logout when they are done updating their progress by selecting **Logout** from the main menu.

### Distinctiveness and Complexity

* I implemented JavaScript Fetch (AJAX) to allow players to check off life goals without interrupting their flow with page reloads.
### File Overview
Here is a list of my main files/folders and what they do:
* **app.py**: The entry point that initializes the app and registers blueprints.
* **auth/**: Handles secure registration (password hashing) and sessions.
* **tracker/**: Contains the core logic for the dynamic generation routes and goal updates.
* **static/script.js**: Manages the AJAX requests for the checkboxes.
* **veggie.db**: The SQLite database containing the 10-generation ruleset. I created four tables in this database.
  * _generations_: This table keeps track of the generation names, color_codes, careers, aspiration, requirements
  * _goals_: This table keeps track of the goals for each generation and references the _generations_ table
  * _user\_progress_: This table keeps track of the users progress on the goals of each generation by referencing the _users_ and _goals_ tables.
  * _users_: This table stores usernames and hash for passwords

The project uses a many-to-many relationship structure between Users and Goals, managed via a _user_progress_ junction table.
### Website Architecture
Unlike simple single-file apps, this project uses Flask Blueprints to separate Authentication from Gameplay logic.
``` .
├── README.md
├── __pycache__
│   ├── app.cpython-310.pyc
│   └── helpers.cpython-310.pyc
├── app.py
├── auth
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── routes.cpython-310.pyc
│   ├── routes.py
│   └── templates
│       ├── login.html
│       └── register.html
├── helpers.py
├── requirements.txt
├── static
│   ├── images
│   │   ├── broccoli.png
│   │   ├── carrot.png
│   │   ├── cauliflower.png
│   │   ├── eggplant.png
│   │   ├── logo.png
│   │   ├── mushroom.png
│   │   ├── pea.png
│   │   ├── potato.png
│   │   ├── radish.png
│   │   ├── squash.png
│   │   └── tomato.png
│   ├── scripts.js
│   └── styles.css
├── templates
│   └── layout.html
├── tracker
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── routes.cpython-310.pyc
│   ├── routes.py
│   └── templates
│       ├── generation.html
│       └── index.html
├── tracker.py
└── veggie.db
```
