import os
import random
from flask import Flask, render_template, request, redirect, session, g, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Data Structure ---
users = {
    'user1@example.com': {'password': 'password', 'description': 'Люблю подорожувати та читати книги.', 'photo': 'user1.jpg', 'hobbies': ['Подорожі', 'Книги'], 'likes_from': set(), 'matches': set()},
    'user2@example.com': {'password': 'password', 'description': 'Фанатка кіно та музики.', 'photo': 'user2.jpg', 'hobbies': ['Кіно', 'Музика'], 'likes_from': set(), 'matches': set()},
    'user3@example.com': {'password': 'password', 'description': 'Займаюся спортом і граю в ігри.', 'photo': 'user3.jpg', 'hobbies': ['Спорт', 'Ігри', 'Кіно'], 'likes_from': set(), 'matches': set()},
    'anna@example.com': {'password': 'password', 'description': 'Програмістка, яка любить гори.', 'photo': 'user4.jpg', 'hobbies': ['Подорожі', 'Ігри'], 'likes_from': set(), 'matches': set()},
    'bob@example.com': {'password': 'password', 'description': 'Шукаю компанію для перегляду фільмів.', 'photo': 'user5.jpg', 'hobbies': ['Кіно', 'Книги'], 'likes_from': set(), 'matches': set()},
    'charlie@example.com': {'password': 'password', 'description': 'Ранкові пробіжки та вечірні серіали.', 'photo': 'user6.jpg', 'hobbies': ['Спорт', 'Кіно'], 'likes_from': set(), 'matches': set()},
    'diana@example.com': {'password': 'password', 'description': 'Музика - моє все. Граю на гітарі.', 'photo': 'user7.jpg', 'hobbies': ['Музика'], 'likes_from': set(), 'matches': set()},
    'eva@example.com': {'password': 'password', 'description': 'Колекціоную вінілові платівки та рідкісні книги.', 'photo': 'user8.jpg', 'hobbies': ['Музика', 'Книги'], 'likes_from': set(), 'matches': set()},
}
HOBBIES = ['Спорт', 'Музика', 'Подорожі', 'Кіно', 'Ігри', 'Книги']

# --- Translations ---
TRANSLATIONS = {
    'Dating App': {'uk': 'Dating App', 'en': 'Dating App'}, 'Привіт': {'uk': 'Привіт', 'en': 'Hello'},
    'Вийти': {'uk': 'Вийти', 'en': 'Logout'}, 'Вхід': {'uk': 'Вхід', 'en': 'Login'},
    'Реєстрація': {'uk': 'Реєстрація', 'en': 'Register'}, 'Пошта': {'uk': 'Пошта', 'en': 'Email'},
    'Пароль': {'uk': 'Пароль', 'en': 'Password'}, 'Увійти': {'uk': 'Увійти', 'en': 'Sign In'},
    'Назад': {'uk': 'Назад', 'en': 'Back'}, 'Зареєструватися': {'uk': 'Зареєструватися', 'en': 'Sign Up'},
    'Неправильна пошта або пароль.': {'uk': 'Неправильна пошта або пароль.', 'en': 'Invalid email or password.'},
    'Пошта та пароль не можуть бути порожніми.': {'uk': 'Пошта та пароль не можуть бути порожніми.', 'en': 'Email and password cannot be empty.'},
    'Користувач з такою поштою вже існує.': {'uk': 'Користувач з такою поштою вже існує.', 'en': 'A user with this email already exists.'},
    'Редагувати профіль': {'uk': 'Редагувати профіль', 'en': 'Edit Profile'}, 'Опис': {'uk': 'Опис', 'en': 'Description'},
    'Фото профілю': {'uk': 'Фото профілю', 'en': 'Profile Picture'}, 'Захоплення': {'uk': 'Захоплення', 'en': 'Hobbies'},
    'Зберегти': {'uk': 'Зберегти', 'en': 'Save'}, 'Спорт': {'uk': 'Спорт', 'en': 'Sports'},
    'Музика': {'uk': 'Музика', 'en': 'Music'}, 'Подорожі': {'uk': 'Подорожі', 'en': 'Travel'},
    'Кіно': {'uk': 'Кіно', 'en': 'Movies'}, 'Ігри': {'uk': 'Ігри', 'en': 'Gaming'},
    'Книги': {'uk': 'Книги', 'en': 'Books'}, 'Лайк': {'uk': 'Лайк', 'en': 'Like'},
    'Свап': {'uk': 'Свап', 'en': 'Swap'}, 'Кандидати закінчились': {'uk': 'Кандидати закінчились', 'en': 'No more matches'},
    'Сповіщення': {'uk': 'Сповіщення', 'en': 'Notifications'}, 'Мої метчі': {'uk': 'Мої метчі', 'en': 'My Matches'},
    'Пошук': {'uk': 'Пошук', 'en': 'Find'}, 'Написати': {'uk': 'Написати', 'en': 'Chat'},
    'У вас новий метч!': {'uk': 'У вас новий метч!', 'en': "It's a Match!"},
    'Продовжити пошук': {'uk': 'Продовжити пошук', 'en': 'Continue Swiping'},
    'Головна': {'uk': 'Головна', 'en': 'Home'}, 'Ласкаво просимо до Dating App!': {'uk': 'Ласкаво просимо до Dating App!', 'en': 'Welcome to Dating App!'},
    'Використовуйте навігацію, щоб знайти нові знайомства.': {'uk': 'Використовуйте навігацію, щоб знайти нові знайомства.', 'en': 'Use the navigation to find new people.'},
    'Почати пошук': {'uk': 'Почати пошук', 'en': 'Start Searching'},
    'Використовуйте навігацію, щоб керувати своїм профілем.': {'uk': 'Використовуйте навігацію, щоб керувати своїм профілем.', 'en': 'Use the navigation to manage your profile.'},
}

# --- Helper Functions ---
def get_user(email):
    return users.get(email)

def get_notifications(user_email):
    user = get_user(user_email)
    if not user: return {}
    my_likes = user.get('likes_from', set())
    likers = {
        email: data for email, data in users.items()
        if user_email in data.get('likes_from', set()) and email not in my_likes
    }
    return likers

def add_like(liker_email, liked_email):
    get_user(liker_email)['likes_from'].add(liked_email)
    if liker_email in get_user(liked_email).get('likes_from', set()):
        get_user(liker_email)['matches'].add(liked_email)
        get_user(liked_email)['matches'].add(liker_email)
        return True
    return False

# --- Translation & Request Handling ---
@app.before_request
def before_request_handler():
    g.locale = session.get('language', 'uk')
    g.user = None
    if 'user_email' in session:
        user = get_user(session['user_email'])
        if user:
            g.user = user
            g.user['email'] = session['user_email']
        else:
            session.clear()

def _(text):
    return TRANSLATIONS.get(text, {}).get(g.locale, text)

app.jinja_env.globals.update(_=_, get_user=get_user, get_notifications=get_notifications)

# --- Main Routes ---
@app.route("/")
def home():
    if not g.user: return render_template("index.html")
    return render_template("home.html")

@app.route('/find_matches')
def find_matches():
    if not g.user: return redirect(url_for('home'))
    if 'match_queue' not in session or not session['match_queue']:
        seen = g.user['likes_from'] | g.user['matches']
        potential = [
            email for email, profile in users.items()
            if email != g.user['email'] and email not in seen
            and any(h in profile.get('hobbies', []) for h in g.user.get('hobbies', []))
        ]
        random.shuffle(potential)
        session['match_queue'] = potential
    next_email = session['match_queue'].pop(0) if session['match_queue'] else None
    session.modified = True
    return render_template('find_matches.html', email=next_email, candidate=get_user(next_email))

# --- Action Routes ---
@app.route('/like/<string:liked_email>')
def like_user(liked_email):
    if not g.user: return redirect(url_for('home'))
    if add_like(g.user['email'], liked_email):
        return redirect(url_for('new_match', matched_email=liked_email))
    if request.referrer and 'notifications' in request.referrer:
        return redirect(url_for('notifications'))
    return redirect(url_for('find_matches'))

@app.route('/swap/<string:swapped_email>')
def swap_user(swapped_email):
    if not g.user: return redirect(url_for('home'))
    return redirect(url_for('find_matches'))

# --- Page Routes ---
@app.route('/notifications')
def notifications():
    if not g.user: return redirect(url_for('home'))
    return render_template('notifications.html', likers=get_notifications(g.user['email']))

@app.route('/my_matches')
def my_matches():
    if not g.user: return redirect(url_for('home'))
    matches_profiles = {email: get_user(email) for email in g.user.get('matches', set())}
    return render_template('my_matches.html', matches=matches_profiles)

@app.route('/new_match/<string:matched_email>')
def new_match(matched_email):
    if not g.user or matched_email not in g.user['matches']: return redirect(url_for('home'))
    return render_template('new_match.html', match=get_user(matched_email), match_email=matched_email)

@app.route('/chat/<string:chat_with_email>')
def chat(chat_with_email):
    if not g.user or chat_with_email not in g.user['matches']: return redirect(url_for('home'))
    return render_template('chat.html', partner=get_user(chat_with_email), partner_email=chat_with_email)

# --- Auth & Profile Routes ---
@app.route("/login", methods=["POST"])
def login():
    email, password = request.form.get("email"), request.form.get("password")
    user = get_user(email)
    if user and user['password'] == password:
        session["user_email"] = email
        return redirect(url_for('home'))
    return render_template("index.html", error=_('Неправильна пошта або пароль.'), form_to_show='login')

@app.route("/register", methods=["POST"])
def register():
    email, password = request.form.get("email"), request.form.get("password")
    if not email or not password:
        return render_template("index.html", error=_('Пошта та пароль не можуть бути порожніми.'), form_to_show='register')
    if get_user(email):
        return render_template("index.html", error=_('Користувач з такою поштою вже існує.'), form_to_show='register')
    users[email] = {'password': password, 'description': '', 'photo': None, 'hobbies': [], 'likes_from': set(), 'matches': set()}
    session["user_email"] = email
    return redirect(url_for('edit_profile'))

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    if not g.user: return redirect(url_for('home'))
    if request.method == 'POST':
        g.user['description'] = request.form.get('description', '')
        g.user['hobbies'] = request.form.getlist('hobbies')
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                g.user['photo'] = filename
        return redirect(url_for('home'))
    return render_template('edit_profile.html', user=g.user, hobbies_list=HOBBIES)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)