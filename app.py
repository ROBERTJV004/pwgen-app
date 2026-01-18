import os
import json
from datetime import date
from flask import Flask, render_template, request, flash, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from generators import generate_password, check_strength


def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Add CSP header
    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self';"
        )
        return response
    
    @app.route('/', methods=['GET', 'POST'])
    @limiter.limit("10 per minute")
    def index():
        password = None
        strength = None
        saved = False
        
        if request.method == 'POST':
            try:
                length = int(request.form.get('length', 12))
                if length <= 0:
                    flash('Length must be greater than 0!', 'error')
                    return render_template('index.html')
                
                include_numbers = request.form.get('include_numbers') == 'on'
                include_symbols = request.form.get('include_symbols') == 'on'
                
                password = generate_password(length, include_numbers, include_symbols)
                strength = check_strength(password)
                
                # Log password generation
                app.logger.info(f"Generated pw len={length} nums={include_numbers} syms={include_symbols}")
                
                # Update stats counter
                _increment_stats_counter(app)
                
                # Save to file if requested
                if request.form.get('save_to_file') == 'on':
                    with open("passwords.txt", "a") as f:
                        f.write(f"{password}\n")
                    saved = True
                    flash('Password saved to passwords.txt!', 'success')
                
            except ValueError:
                flash('Please enter a valid number for length!', 'error')
                return render_template('index.html')
        
        return render_template('index.html', password=password, strength=strength, saved=saved)
    
    @app.route('/stats')
    def stats():
        """Display statistics page"""
        count = _get_today_count()
        stats_data = _get_full_stats()
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Password Generator Stats</title>
            <style>
                body {{
                    font-family: sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
                h1 {{
                    color: #007bff;
                    text-align: center;
                }}
                .stat {{
                    font-size: 1.5em;
                    text-align: center;
                    margin: 20px 0;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                a {{
                    display: block;
                    text-align: center;
                    margin-top: 20px;
                    color: #007bff;
                    text-decoration: none;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background: #28a745;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
                .button:hover {{
                    background: #218838;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Password Generator Stats</h1>
                <div class="stat">Total generations today: <strong>{count}</strong></div>
                <div style="text-align: center;">
                    <a href="/stats/download" class="button">Download Stats JSON</a>
                </div>
                <a href="/">← Back to Generator</a>
            </div>
        </body>
        </html>
        """
    
    @app.route('/stats/download')
    def stats_download():
        """Download stats as JSON file"""
        stats_data = _get_full_stats()
        return jsonify(stats_data), 200, {
            'Content-Type': 'application/json',
            'Content-Disposition': 'attachment; filename=password_stats.json'
        }
    
    def _get_stats_file():
        """Get path to stats file"""
        return "stats.json"
    
    def _get_today_count():
        """Get count of password generations today"""
        stats_file = _get_stats_file()
        today = str(date.today())
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    if stats.get('date') == today:
                        return stats.get('count', 0)
        except (json.JSONDecodeError, IOError):
            pass
        
        return 0
    
    def _get_full_stats():
        """Get full stats data"""
        stats_file = _get_stats_file()
        today = str(date.today())
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    return {
                        'date': stats.get('date', today),
                        'count': stats.get('count', 0),
                        'current_date': today
                    }
        except (json.JSONDecodeError, IOError):
            pass
        
        return {
            'date': today,
            'count': 0,
            'current_date': today
        }
    
    def _increment_stats_counter(app_instance):
        """Increment the stats counter for today"""
        stats_file = _get_stats_file()
        today = str(date.today())
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
            else:
                stats = {}
            
            if stats.get('date') == today:
                stats['count'] = stats.get('count', 0) + 1
            else:
                stats = {'date': today, 'count': 1}
            
            with open(stats_file, 'w') as f:
                json.dump(stats, f)
        except (json.JSONDecodeError, IOError) as e:
            app_instance.logger.error(f"Error updating stats: {e}")
    
    return app
