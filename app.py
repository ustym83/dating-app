from flask import Flask, render_template, request, redirect, session, g

app = Flask(__name__)
app.secret_key = "super_secret_key"

# --- Custom Translation System ---
LANGUAGES = ['uk', 'en']

TRANSLATIONS = {
    'Dating App': {
        'uk': 'Dating App',
        'en': 'Dating App'
    },
    'Список користувачів': {
        'uk': 'Список користувачів',
        'en': 'User List'
    },
    'Привіт': {
        'uk': 'Привіт',
        'en': 'Hello'
    },
    'Вийти': {
        'uk': 'Вийти',
        'en': 'Logout'
    },
    'Вхід': {
        'uk': 'Вхід',
        'en': 'Login'
    },
    'Реєстрація': {
        'uk': 'Реєстрація',
        'en': 'Register'
    },
    'Пошта': {
        'uk': 'Пошта',
        'en': 'Email'
    },
    'Пароль': {
        'uk': 'Пароль',
        'en': 'Password'
    },
    'Увійти': {
        'uk': 'Увійти',
        'en': 'Sign In'
    },
    'Назад': {
        'uk': 'Назад',
        'en': 'Back'
    },
    'Зареєструватися': {
        'uk': 'Зареєструватися',
        'en': 'Sign Up'
    },
    'Неправильна пошта або пароль.': {
        'uk': 'Неправильна пошта або пароль.',
        'en': 'Invalid email or password.'
    },
    'Пошта та пароль не можуть бути порожніми.': {
        'uk': 'Пошта та пароль не можуть бути порожніми.',
        'en': 'Email and password cannot be empty.'
    },
    'Користувач з такою поштою вже існує.': {
        'uk': 'Користувач з такою поштою вже існує.',
        'en': 'A user with this email already exists.'
    }
}

def get_locale():
    if 'language' in session and session['language'] in LANGUAGES:
        return session['language']
    return 'uk' # Default language

def _(text):
    locale = get_locale()
    if text in TRANSLATIONS and locale in TRANSLATIONS[text]:
        return TRANSLATIONS[text][locale]
    return text # Fallback to original text if no translation found

# Впроваджуємо функцію _() в шаблони Jinja
app.jinja_env.globals.update(_=_)

@app.before_request
def before_request():
    g.locale = get_locale()
# --- End Custom Translation System ---


# Словник для зберігання користувачів: email -> password
users = {}

@app.route("/")
def home():
    return render_template("index.html", users=list(users.keys()))

@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    # If the referrer is None, redirect to home
    return redirect(request.referrer or "/")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if email in users and users[email] == password:
        session["user"] = email
        return redirect("/")
    else:
        error_message = _('Неправильна пошта або пароль.')
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error=error_message,
                               form_to_show='login')

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        error_message = _('Пошта та пароль не можуть бути порожніми.')
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error=error_message,
                               form_to_show='register')

    if email not in users:
        users[email] = password
        session["user"] = email
        return redirect("/")
    else:
        error_message = _('Користувач з такою поштою вже існує.')
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error=error_message,
                               form_to_show='register')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)