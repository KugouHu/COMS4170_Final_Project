# COMS4170 Final Project — Zodiac Constellations

An interactive web guide to the 12 zodiac constellations, built with Flask. Users enter their name and birthday to discover their zodiac sign, browse all 12 constellations, learn about each one, and test their knowledge with a quiz.

## Features

- **Personalized start page** — enter your name and birthday to identify your zodiac sign
- **Home dashboard** — browse all 12 constellations as cards, with your personal sign highlighted
- **Learn pages** — detailed information on each constellation's star pattern and how to find it in the sky
- **Quiz** — test your zodiac knowledge

## Tech Stack

- **Backend:** Flask 3.1.3 (Python 3.12+)
- **Frontend:** Bootstrap 5.3, jQuery 3.6, Jinja2 templates
- **Styling:** Custom CSS with hover/highlight effects for constellation cards

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/KugouHu/COMS4170_Final_Project.git
cd FINAL_HTML
```

### 2. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The app will start at `http://127.0.0.1:5000`.

## Project Structure

```
FINAL_HTML/
├── app.py              # Flask application entry point & routes
├── requirements.txt    # Python dependencies (Flask)
├── static/
│   ├── style.css       # Custom styles (constellation cards, highlights)
│   └── main.js         # Client-side helpers (image fallbacks)
├── templates/
│   ├── start.html      # Landing page — name & birthday form
│   └── home.html       # Dashboard — grid of 12 zodiac constellation cards
└── README.md
```