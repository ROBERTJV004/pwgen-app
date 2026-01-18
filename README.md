# Password Generator Web App

A secure password generator built with Flask, ready to deploy on Render.

## Features

- Generate secure passwords with customizable length
- Option to include numbers and symbols
- Password strength indicator
- Save passwords to file
- Beautiful, modern web interface

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python3 run.py
```

3. Run tests:
```bash
pytest
```

4. Open your browser to `http://localhost:5000`

## Deploying to Render

1. Push your code to GitHub

2. On Render:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: password-generator (or your choice)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python run.py`
   - Click "Create Web Service"

3. Render will automatically:
   - Set the `PORT` environment variable
   - Deploy your app
   - Give you a URL like `https://your-app.onrender.com`

## Environment Variables (Optional)

- `SECRET_KEY`: Flask secret key for sessions (Render can generate this)
- `PORT`: Automatically set by Render (don't set manually)

## Project Structure

```
pwgen-app/
├── app.py              # Flask factory with routes
├── generators.py       # Password generation logic
├── run.py              # Application entry point
├── templates/
│   └── index.html      # Web interface
├── tests/
│   └── test_generators.py  # Unit tests
├── requirements.txt    # Python dependencies
└── PasswordGen.py      # Original console version (reference)
```

## Files

- `app.py`: Flask application factory with routes
- `generators.py`: Password generation and strength checking functions
- `run.py`: Entry point to run the application
- `templates/index.html`: Web interface template
- `tests/test_generators.py`: Unit tests for password generation
- `requirements.txt`: Python dependencies
- `PasswordGen.py`: Original console version (kept for reference)
