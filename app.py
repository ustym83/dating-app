import os
from flask import Flask, render_template, request, redirect, session, g, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Custom Translation System ---
LANGUAGES = ['uk', 'en']
TRANSLATIONS = {
    # ... (previous translations)
    'Dating App': {'uk': 'Dating App', 'en': 'Dating App'},
    'Список користувачів': {'uk': 'Список користувачів', 'en': 'User List'},
    'Привіт': {'uk': 'Привіт', 'en': 'Hello'},
    'Вийти': {'uk': 'Вийти', 'en': 'Logout'},
    'Вхід': {'uk': 'Вхід', 'en': 'Login'},
    'Реєстрація': {'uk': 'Реєстрація', 'en': 'Register'},
    'Пошта': {'uk': 'Пошта', 'en': 'Email'},
    'Пароль': {'uk': 'Пароль', 'en': 'Password'},
    'Увійти': {'uk': 'Увійти', 'en': 'Sign In'},
    'Назад': {'uk': 'Назад', 'en': 'Back'},
    'Зареєструватися': {'uk': 'Зареєструватися', 'en': 'Sign Up'},
    'Неправильна пошта або пароль.': {'uk': 'Неправильна пошта або пароль.', 'en': 'Invalid email or password.'},
    'Пошта та пароль не можуть бути порожніми.': {'uk': 'Пошта та пароль не можуть бути порожніми.', 'en': 'Email and password cannot be empty.'},
    'Користувач з такою поштою вже існує.': {'uk': 'Користувач з такою поштою вже існує.', 'en': 'A user with this email already exists.'},
    'Редагувати профіль': {'uk': 'Редагувати профіль', 'en': 'Edit Profile'},
    'Опис': {'uk': 'Опис', 'en': 'Description'},
    'Фото профілю': {'uk': 'Фото профілю', 'en': 'Profile Picture'},
    'Захоплення': {'uk': 'Захоплення', 'en': 'Hobbies'},
    'Зберегти': {'uk': 'Зберегти', 'en': 'Save'},
    'Спорт': {'uk': 'Спорт', 'en': 'Sports'},
    'Музика': {'uk': 'Музика', 'en': 'Music'},
    'Подорожі': {'uk': 'Подорожі', 'en': 'Travel'},
    'Кіно': {'uk': 'Кіно', 'en': 'Movies'},
    'Ігри': {'uk': 'Ігри', 'en': 'Gaming'},
    'Книги': {'uk': 'Книги', 'en': 'Books'},
}

def get_locale():
    if 'language' in session and session['language'] in LANGUAGES:
        return session['language']
    return 'uk'

def _(text):
    locale = get_locale()
    if text in TRANSLATIONS and locale in TRANSLATIONS[text]:
        return TRANSLATIONS[text][locale]
    return text

app.jinja_env.globals.update(_=_)

@app.before_request
def before_request():
    g.locale = get_locale()
    # Якщо користувач є в сесії, але його немає в базі даних (після перезапуску)
    if 'user' in session and session['user'] not in users:
        session.pop('user') # Очищуємо недійсну сесію
# --- End Custom Translation System ---


# --- Data Structure ---
# users = { 'email': {'password': '...', 'description': '...', 'photo': '...', 'hobbies': [...] } }
users = {}
HOBBIES = ['Спорт', 'Музика', 'Подорожі', 'Кіно', 'Ігри', 'Книги']


@app.route("/")
def home():
    if 'user' not in session:
        return render_template("index.html")
    
    # Pass user objects to the template, excluding the current user
    other_users = {email: profile for email, profile in users.items() if email != session.get('user')}
    return render_template("home.html", users=other_users)

@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(request.referrer or "/")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if email in users and users[email]['password'] == password:
        session["user"] = email
        return redirect("/")
    else:
        return render_template("index.html", error=_('Неправильна пошта або пароль.'), form_to_show='login')

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return render_template("index.html", error=_('Пошта та пароль не можуть бути порожніми.'), form_to_show='register')

    if email not in users:
        users[email] = {
            'password': password,
            'description': '',
            'photo': None,
            'hobbies': []
        }
        session["user"] = email
        return redirect(url_for('edit_profile')) # Redirect to profile creation
    else:
        return render_template("index.html", error=_('Користувач з такою поштою вже існує.'), form_to_show='register')

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect('/')
    
    email = session['user']
    
    if request.method == 'POST':
        users[email]['description'] = request.form.get('description', '')
        users[email]['hobbies'] = request.form.getlist('hobbies')
        
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                users[email]['photo'] = filename
        
        return redirect(url_for('home'))

    # Переконуємось, що користувач все ще існує в 'users'
    if email not in users:
        return redirect(url_for('logout'))

    return render_template('edit_profile.html', user=users[email], hobbies_list=HOBBIES)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("language", None) # Також очищуємо мову при виході
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)