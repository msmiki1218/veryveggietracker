# VERY VEGGIE TRACKER
#### Video Demo: [https://youtu.be/UFNapAqmcnE](https://youtu.be/UFNapAqmcnE)
#### Description: A specialized web application for tracking the 10-generation Sims 4 "Very Veggie Legacy Challenge" by lilsimsie.

## Project Motivation
Selecting a final project topic was a journey of finding the intersection between personal interest and technical utility. As an active player of the **Very Veggie Legacy Challenge**, I initially tracked my progress using spreadsheets. However, as the gameplay grew more complex, the manual tracking became cumbersome.

Drawing inspiration from the CS50 Finance problem set and brainstorming sessions with [Gemini](https://gemini.google.com/app), I saw an opportunity to streamline this experience. I decided to build a dedicated web application using **Python, Flask, SQLite3, and Jinja2**, transforming a manual process into a structured, user-friendly digital tracker.

## Features
* **Interactive Dashboard:** Dynamic progress bars that update as you complete goals.
* **Full-Stack Interactivity:** Uses JavaScript `Fetch API` to update the database without page reloads.
* **Sims Aesthetic:** Clean UI built with W3.CSS, featuring custom 3D-style vegetable icons.
* **Secure Auth:** Session-based login and registration with inline error handling.

## How It Works
1. Authentication & Security
   * **Access:** Users begin at the **Login** page. Existing users can authenticate with their credentials.
   * **Onboarding:** New users can navigate to the **Register** page. The system ensures data integrity by preventing duplicate usernames. Once registered, users are redirected to log in and begin their session.
2. The Dashboard (Progress at a Glance)
  Upon logging, users are greeted by a personalized **Dashboard**.
   * **Generation Cards:** Each stage of the Legacy Challenge is represented by a dedicated card.
   * **Visual Tracking:** Each card features a dynamic progress bar that calculates the percentage of completed requirements for that specific generation in real-time.
3. Tracking Progress
   * **Requirement Lists:** Clicking a card opens a detailed subpage listing all specific requirements for that generation.
   * **Interactive Updates:** Users can check off tasks as they complete them. Thanks to the SQLite3 backend, these updates are saved instantly.
   * **Dynamic Feedback:** When returning to the Dashboard, the progress bars automatically reflect the new completion data.
4. Session Management
   * Users can securely end their session at any time by selecting **Logout** from the navigation menu, ensuring their data remains private.

## How to Run
To run this project locally, ensure you have **Python 3** and `pip` installed. Follow these steps to get your environment ready:

### 1. Clone the Repository
  ```bash
  git clone https://github.com/msmiki1218/veryveggietracker.git
  cd veryveggietracker
  ```
### 2. Install Dependencies
  It is recommended to use a virtual environment. Once activated, install the required packages:
  ```bash
  pip install -r requirements.text
  ```

### 3. Initialize the Database
  Ensure the `veggie.db` is in the root directory. If you have a schema setup script run it now:
  ```bash
  sqlite3 veggie.db < schema.sql
  ```

### 4. Start the Flask Server
  Run the application using the Flask CLI:
  ```bash
  flask run
  ```

Once the server is active, open your browser and navigate to to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Technology Stack
* **Backend:** Python/Flask
* **Database:** SQLite3
* **Frontend:** Jinja2 Templates, W3.CSS, Vanilla JavaScript
* **Assets:** Custom AI-generated 3D Vegetable Graphics

## Implementation Details

The development of this tracker focused on creating a secure, scalable, and dynamic user experience. Below are the key technical implementations:

### 1. User Authentication & Security
Following the security standards established in the CS50 Finance project, this application prioritizes user data protection:
* **Password Security:** Passwords are never stored in plain text. Instead, I utilized `werkzeug.security` to implement `generate_password_hash` for registration and `check_password_hash` for login verification.
* **Session Management:** I used the `flask-session` library to handle server-side session storage. A custom `@login_required` decorator ensures that sensitive routes—like the dashboard and progress tracking pages—are inaccessible to unauthenticated users.

### 2. Frontend Design with W3.CSS
To create a clean and responsive user interface, I utilized the **W3.CSS framework**. 
* **Lightweight Responsiveness:** W3.CSS allowed for a mobile-friendly dashboard without the heavy footprint of larger libraries. I specifically leveraged the grid system to ensure the "Generation Cards" wrap correctly on different screen sizes.
* **Visual Progress Feedback:** I used W3.CSS progress bar classes (`w3-container`, `w3-grey`) combined with inline dynamic widths calculated by the backend to provide immediate visual feedback on challenge completion.

### 3. Dynamic Routing with Jinja2
To keep the codebase **DRY (Don't Repeat Yourself)**, I implemented dynamic routing for the various challenge generations. 
* Instead of creating 10+ separate HTML files, a single `@app.route("/generation/<int:id>")` captures the generation number from the URL.
* This ID triggers a SQL query to fetch the relevant requirements from the database, which are then injected into a universal `generation.html` template using **Jinja2** logic.

### 4. State Persistence & Logic
A major upgrade from the previous spreadsheet method was the transition to a relational database for state management:
* **Junction Table Logic:** I utilized a `user_progress` table to create a many-to-many relationship between users and requirements. 
* **Real-time Calculation:** The dashboard calculates progress programmatically upon every load using the following logic:

$$\text{Progress \%} = \left( \frac{\text{COUNT(completed\_tasks)}}{\text{COUNT(total\_tasks\_in\_gen)}} \right) \times 100$$

## Database Schema

The application uses **SQLite3** to manage user data and challenge progress. The database is designed with a relational structure to ensure data integrity and to keep user progress isolated.

### Entity Relationship Overview
The database uses a relational structure to connect users to their specific task completions. By using foreign keys, the app maintains data integrity and ensures that one user’s progress never interferes with another’s.

### Table Definitions

| Table | Key Columns | Description |
| :--- | :--- | :--- |
| **`users`** | `id`, `username`, `hash` | Stores unique user credentials and hashed passwords. |
| **`generations`** | `id`, `name` | Defines the various stages of the Very Veggie Legacy Challenge. |
| **`goals`** | `id`, `generation_id`, `description` | Contains the specific goals tied to each generation via foreign key. |
| **`user_progress`** | `user_id`, `req_id`, `completed` | A junction table tracking which requirements a user has completed. |

## File Overview
Here is a list of my main files/folders and what they do:
* **app.py**: The entry point that initializes the app and registers blueprints.
* **auth/**: Handles secure registration (password hashing) and sessions.
* **tracker/**: Contains the core logic for the dynamic generation routes and goal updates.
* **static/script.js**: Manages the AJAX requests for the checkboxes.
* **veggie.db**: The SQLite3 database containing the 10-generation ruleset. The database consists of the following tables linked by foreign keys:
  * _generations_: A static table (or predefined list) containing the metadata for each stage of the Very Veggie Challenge.
  * _goals_: Tracks the specific tasks for each generation.
  * _user\_progress_: The junction table that records which user has completed which requirement, allowing for the dynamic calculation of the progress bars seen on the dashboard.
  * _users_: Stores unique credentials and hashed passwords.

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
## Technical Challenges
Building this tracker presented a few key learning moments:
* **Dynamic Progress Calculation:** The biggest challenge was ensuring the progress bars updated immediately without reloading the entire page logic. This required a clean SQL `JOIN` between the `goals` and `user_progress` tables to calculate percentages on the fly.
* **Data Integrity:** Implementing the registration system required careful handling of the SQLite constraints to ensure that duplicate usernames could not be created, provinding a smooth error-handling experience for the user.
* **State Management:** Transitioning from a static spreadsheet to a dynamic web app meant rethinking how "checked" items are stored. Using a junction table for user progress proved much more efficient than storing arrays of data.

## Future Improvements

While the current version of the tracker successfully manages the core requirements of the Very Veggie Legacy Challenge, I plan to implement the following features in future iterations:

### 1. Social Sharing & Community Features
* **Public Profiles:** Allow users to make their dashboards public so they can share their progress with the Sims community.
* **Progress Snapshots:** Generate a "Legacy Card" image using a library like `Pillow` that users can download and post on social media to showcase their completed generations.

### 2. Enhanced Data Visualization
* **Challenge Timeline:** Implement a horizontal timeline view using JavaScript (e.g., Chart.js) to show the history of when each generation was started and completed.
* **Detailed Statistics:** Add a "Stats" page to track metrics like "Total Requirements Met" or "Fastest Generation Completed."



### 3. User Experience & Customization
* **Dark Mode:** Implement a theme toggle using CSS variables to switch between light and dark modes for late-night gaming sessions.
* **Custom Challenge Creation:** Allow users to input their own custom legacy challenge rules into the database, transforming the app into a universal Sims challenge tracker.
* **Image Uploads:** Integrate an AWS S3 bucket or local storage to allow users to upload a "Heir Photo" for each generation card on the dashboard.



### 4. Notification System
* **Goal Reminders:** Implement a notification system that alerts the user when they are only one requirement away from completing a generation.

## Acknowledgements
- **Challenge Creator:** [lilsimsie](https://www.youtube.com/lilsimsie) for the Very Veggie Legacy Challenge rules.
- **CS50x:** For the foundational knowledge and the 'Finance' pset inspiration.
- **Gemini:** For brainstorming and project structure assistance.