# Waste Management MVP

This repository contains an exploratory waste-management MVP combining:
- a Flask-based web interface for item intake and disposal guidance
- an analytics dashboard for textile recycling locations
- reusable content and resources for waste reduction and reuse

## Requirements
- Python 3.10+
- `requirements.txt` defines the required Python dependencies

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Running locally
Start the application with:
```bash
python app/website.py
```

Then open `http://localhost:5000` in your browser.

## Project structure
- `app/` – Flask application, analytics dashboard, and helper modules
- `templates/` – HTML templates for the website views
- `static/` – static assets and uploaded files
- `data/branch_cache/` – cached branch location data from OpenStreetMap

## Development instance
A development deployment is available on [Render](https://render.com/). Visit the registered instance [URL](waste-manager-qhpm.onrender.com) from the project description in the Render dashboard.

## Notes
- The application currently uses in-memory storage for users and items.
- Analytics routes are mounted under `/analytics/` via Dash.
- External scraping logic may require valid target URLs and robots.txt compliance.
