# HISTOFACTS

HISTOFACTS is an interactive Streamlit web application that helps users explore historical events by date, search topics, view timelines, take quizzes, and save favorites/bookmarks. It combines a clean UI with optional LLM-powered quiz generation and a simple, session-backed user system.

## Features

- User registration & login (MySQL-backed)
- Historical Dashboard: "Today in History" and categorized daily events
- Timeline view and categorized tabs
- Search across historical topics/events
- Quiz system: 10-question multiple-choice quizzes (Gemini/LLM-powered with fallback samples)
- Favorites & Bookmarks: save interesting events

## Quick Start

1. Clone the repo
   ```bash
   git clone https://github.com/Oriacgz/HistoFacts-Streamlit-.git
   cd HistoFacts-Streamlit-
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell)
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   - Copy and edit the template:
     ```bash
     cp .env.template .env
     ```
   - Set DB_HOST, DB_USER, DB_PASSWORD, DB_NAME and GEMINI_API_KEY in `.env`.
   - Important: remove any hard-coded secrets from source files and keep .env out of commits.

5. Initialize the database (example)
   - Create the database and a `users` table used by authentication:
     ```sql
     CREATE DATABASE IF NOT EXISTS mini CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     USE mini;

     CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

6. Run the app
   ```bash
   streamlit run main.py
   ```
   Open http://localhost:8501 in your browser.

## Project layout

```
.
├─ .env.template           # Example env variables
├─ LICENSE                 # MIT license for this repository
├─ README.md               # (this file)
├─ main.py                 # Streamlit entrypoint / session routing
├─ requirements.txt        # Python dependencies
├─ assets/                 # Images and icons (e.g., icon.png, quiz.png)
├─ pages/
│  ├─ login.py             # Signup / login, DB connection, password hashing
│  ├─ dashboard.py         # Main UI, timeline, favorites/bookmarks, search
│  └─ quiz.py              # Quiz UI and LLM integration / fallback
├─ utils/                  # helper modules (e.g., historical API)
├─ data/                   # optional datafiles
├─ static/                 # static css/js if needed
└─ myenv/                  # local virtualenv (remove from repo)
```

How it fits together:
- `main.py` creates and initializes Streamlit session_state and routes to subpages under `pages/`.
- `pages/login.py` contains user management and the database connection functions.
- `pages/dashboard.py` implements the main UI: shows events, timeline, favorites and bookmarks.
- `pages/quiz.py` generates quizzes (via an LLM if configured) and provides a sample fallback if the API is unavailable.

## Configuration notes & security

- .env variables:
  - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME — MySQL credentials for authentication
  - GEMINI_API_KEY — Optional: enables LLM-based quiz generation

- Security best practices:
  - Do not commit .env or any secrets. Add `.env` (and local virtualenv folders like `myenv/`, `.venv/`) to `.gitignore`.
  - Replace any placeholder or hard-coded API keys and DB credentials found in the code with environment variables.
  - Store user data securely if you move from session-only persistence to a production database.

## Dependencies

See `requirements.txt` — notable packages:
- streamlit
- pandas
- plotly
- pymysql
- bcrypt
- python-dotenv
- google-generativeai (optional for quiz generation)

## Troubleshooting

- Database connection failures: ensure MySQL is running and credentials in `.env` match; test with a DB client.
- If LLM quiz generation fails, the app uses sample questions defined in `pages/quiz.py`.
- Missing images: ensure `assets/icon.png` and `assets/quiz.png` exist, or update references in code.

## Development & testing

- Add unit tests for business logic (e.g., password hashing, question parsing).
- Consider extracting DB access to a small module and adding migrations or seed scripts for easy setup.
- Remove `myenv/` from the repository; add `myenv/` or `.venv/` to `.gitignore`.

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Implement & test locally
4. Open a pull request describing changes

## License

This project is released under the MIT License — see `LICENSE` in the repository (Copyright 2026 Apoorva Puranik).

## Contact

Repository owner: Oriacgz — open an issue or PR on GitHub for questions or features.
