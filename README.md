# COMS4170 Final Project — Zodiac Constellations

An interactive web guide to the 12 zodiac constellations, built with Flask. Users enter their name and birthday to discover their zodiac sign, browse all 12 constellations, learn the details of each one, and test their knowledge with a short quiz.

## Features

- **Personalized start page** — enter your name and birthday to identify your zodiac sign
- **Profile dropdown** — top-right navbar shows a gold avatar with your initial, name, and formatted birthday; a "Switch Profile" option clears your session and returns to the start page
- **Home dashboard** — all 12 constellations shown as cards, with your personal sign highlighted
- **Learn pages** — per-constellation details including description, key stars (with magnitudes), how to find it in the sky, and a fun fact, with prev/next navigation through all 12
- **Randomized quiz** — 10-question bank drawn from the learn content; each attempt randomly selects 5 questions, so retaking the quiz yields a fresh mix
- **Results page** — per-question score, correct/incorrect indicator, and an explanation for the answer you chose

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
python server.py
```

The app will start at `http://127.0.0.1:5000`.

## Routes

- `/` — Start page: name & birthday form; redirects to `/home` once submitted
- `/switch` — Clears the current session and redirects back to `/` (used by the profile dropdown's "Switch Profile" action)
- `/home` — Dashboard with the 12 constellation cards
- `/learn/<n>` — Learn page for constellation `n` (1–12)
- `/quiz/<n>` — Quiz question `n` (1–5 of the randomly selected subset). On entry to `/quiz/1` with no in-progress attempt (or after a completed quiz), 5 questions are freshly drawn from the 10-question bank.
- `/quiz/<n>/answer` — POST handler that records the chosen answer and advances
- `/result` — Final score and per-question review for the 5 questions attempted

## Quiz Randomization

The quiz bank in `server.py` (`data["quiz"]`) holds **10 questions**. Each new attempt calls `pickQuizQuestions()`, which uses `random.sample` to draw 5 questions for the user's session and resets answer state. The `QUIZ_LENGTH` constant at the top of `server.py` controls how many are drawn — change it (and the bank size) if you want a different ratio. Re-shuffling is triggered when the start form is submitted and when the user revisits `/quiz/1` after completing the previous attempt (e.g., via the **Retake Quiz** button on the results page).

## Project Structure

```
FINAL_HTML/
├── server.py           # Flask app: routes, constellation/quiz data, zodiac logic
├── requirements.txt    # Python dependencies (Flask)
├── static/
│   ├── style.css       # Custom styles (constellation cards, highlights)
│   └── main.js         # Client-side helpers (image fallbacks)
├── templates/
│   ├── navbar.html     # Shared top navigation
│   ├── start.html      # Landing page — name & birthday form
│   ├── home.html       # Dashboard — grid of 12 zodiac constellation cards
│   ├── learn.html      # Per-constellation detail page
│   ├── quiz.html       # Quiz question page
│   └── result.html     # Quiz results & review
└── README.md
```
