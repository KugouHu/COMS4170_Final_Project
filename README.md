# COMS4170 Final Project

A web application built with Flask.

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd FINAL_HTML
```

Replace `<your-repo-url>` with the actual GitHub repository URL.

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
├── app.py            # Flask application entry point
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
├── requirements.txt  # Python dependencies
└── README.md
```