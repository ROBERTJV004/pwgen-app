import random
import string
import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

def check_strength(password):
    """Check password strength based on length"""
    if len(password) < 6:
        return "Weak"
    elif len(password) < 10:
        return "Medium"
    else:
        return "Strong"

def generate_password(length, include_numbers, include_symbols):
    """Generate a random password based on user preferences"""
    password = ""
    chars = string.ascii_letters
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation
    for i in range(length):
        password += random.choice(chars)
    return password

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
