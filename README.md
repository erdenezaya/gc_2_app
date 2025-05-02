# Habit Tracker Web App

This is a Flask-based web application that helps users track their daily habits and visualize their progress over time. It is designed to be lightweight, user-friendly, and insightful for anyone looking to improve their routines or build new ones.

## Features (To Be Added)

- 📝 Register and log in to your account
- ➕ Add custom habits to track (e.g., sleep, steps, diet)
- 📈 Upload or log daily habit data
- 📊 Visualize your habits with graphs and charts
- 🤝 Share specific insights or stats with other users
- 🔒 Privacy-aware: your data is private by default

## Tech Stack

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS, Bootstrap, jQuery
- **Database:** SQLite (via SQLAlchemy)
- **Interactivity:** AJAX
- **Version Control:** Git + GitHub

## Getting Started (To Be Added)
This section will include how to launch the application.

1. git clone …
2. cd gc_2_app/habit_tracker
3. python -m venv venv && source venv/bin/activate
4. pip install -r requirements.txt
5. export FLASK_APP=app.py          
6. flask db upgrade             
7. (optional) python scripts/seed.py 
8. flask run

## Testing (To Be Added)
This section will include how to run unit tests, if applicable.

## Project Structure (Updated)
```
gc_2_app/                            ← GitHub repository directory
├── habit_tracker/               ← Flask main application folder
│   ├── app/                     ← your main Flask application code
│   │   ├── __init__.py          ← initialization file
│   │   ├── blueprints/          ← modular Flask blueprints
│   │   │   ├── auth/            ← authentication-related routes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes.py
│   │   │   └── main/            ← main application routes
│   │   │       ├── __init__.py
│   │   │       ├── routes.py
│   │   ├── models.py            ← database models and tables
│   │   ├── forms.py             ← forms for user input
│   │   ├── templates/           ← HTML templates for rendering pages
│   │   │   └── index.html
│   │   └── static/              ← CSS, images, JavaScript files
│   │       ├── css/             ← CSS files for styling
│   │       │   └── style.css    ← additional styles
│   │       ├── js/              ← JavaScript files for interactivity
│   ├── migrations/              ← database migration files
│   ├── scripts/                 ← utility scripts (e.g., seed.py)
│   ├── tests/                   ← test files go here
│   ├── requirements.txt         ← list of Python packages
│   └── app.py                   ← main Flask application entry point
├── deliverables/               ← intermediate presentation materials
├── README.md                   ← info about your project
├── venv/                       ← local virtual environment (do not upload to GitHub)
└── .gitignore                  ← ignore development files in venv/ etc.
```

##  Database Management Scripts

To change SQLAlchemy models by updating app/models.py, the following steps needs to be taken
Below is the recommended **“backup → migrate → upgrade → backup → restore”** workflow:

1. Backup (`python scripts/backup_db.py`)
2. Edit your models.py
3. Migrate (`flask db migrate -m "Describe your change here"`)
4. Review & Commit the new script (`git add migrations/versions/<revision_id>_*.py`, `git commit -m "Migration: <brief description>"`)
5. Upgrade (`flask db upgrade`)
6. Backup (`python scripts/backup_db.py`) - This creates a timestamped file in backups/ reflecting your new schema + data. And push your changes to the GitHub.
7. Restore (`python scripts/restore_db.py`) - After they pull your commits (migrations + new backup), they run this to replace their local app/app.db with the freshest backup.

To keep your local SQLite database in sync, backed up, and pre-populated, we provide three helper scripts in the `scripts/` folder:

| Script               | Purpose                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| `backup_db.py`       | Snapshot your current `app/app.db` into a timestamped file under `backups/` |
| `seed.py`            | Create a “seed” user and habit records so a fresh database isn’t empty.     |
| `restore_db.py`      | Restore the most recent backup over `app/app.db` for quick rollbacks.       |


### 1. `scripts/backup_db.py`
Creates a copy of your live database at `app/app.db` and writes it to `backups/app_YYYYMMDD_HHMMSS.db`.

```bash
# from the project root (where habit_tracker/ lives)
cd habit_tracker
python scripts/backup_db.py
```
### 2. `scripts/restore_db.py`
This solution for keeping historical data in the system to show proper UI/UX. This script finds latest newest app.db file in backups/
and copy it to app/app.db .

```bash
# from the project root
cd habit_tracker
python scripts/restore_db.py
```

### 3. `scripts/seed.py`
If you need initializes your schema with seed user and starter habits, Run this script by following command from project's root folder.

```bash
# from the project root
cd habit_tracker
python scripts/seed.py
```

## Team Members

| Name                    | UWA ID     | GitHub Username  |
|-------------------------|------------|------------------|
| Siqi Shen               | 24117655   |    saltsoda7     |
| Fiona Wei               | 24610193   |    fifibox       |
| Zaya Batnasan           | 24448191   |  erdenezaya      |
| Divyanshu Brijesh Singh | 24322871   |  Divyanshus123   |

