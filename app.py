import os
import random
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
    'Лайк': {'uk': 'Лайк', 'en': 'Like'},
    'Свап': {'uk': 'Свап', 'en': 'Swap'},
    'Кандидати закінчились': {'uk': 'Кандидати закінчились', 'en': 'No more matches'},
    'Сповіщення': {'uk': 'Сповіщення', 'en': 'Notifications'},
    'Мої метчі': {'uk': 'Мої метчі', 'en': 'My Matches'},
    'Пошук': {'uk': 'Пошук', 'en': 'Find'},
    'Написати': {'uk': 'Написати', 'en': 'Chat'},
    'У вас новий метч!': {'uk': 'У вас новий метч!', 'en': "It's a Match!"},
    'Продовжити пошук': {'uk': 'Продовжити пошук', 'en': 'Continue Swiping'},
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
    if 'user' in session:
        if session['user'] not in users:
            session.clear()
        else:
            # Add user object to g for easy access in templates
            g.user_data = users[session['user']]
    else:
        g.user_data = None

# --- Data Structure ---
users = {
    'user1@example.com': {'password': 'password', 'description': 'Люблю подорожувати та читати книги.', 'photo': 'user1.jpg', 'hobbies': ['Подорожі', 'Книги'], 'likes_received': [], 'matches': []},
    'user2@example.com': {'password': 'password', 'description': 'Фанатка кіно та музики.', 'photo': 'user2.jpg', 'hobbies': ['Кіно', 'Музика'], 'likes_received': [], 'matches': []},
    'user3@example.com': {'password': 'password', 'description': 'Займаюся спортом і граю в ігри.', 'photo': 'user3.jpg', 'hobbies': ['Спорт', 'Ігри', 'Кіно'], 'likes_received': [], 'matches': []},
}
HOBBIES = ['Спорт', 'Музика', 'Подорожі', 'Кіно', 'Ігри', 'Книги']


@app.route("/")
def home():
    if 'user' not in session:
        return render_template("index.html")
    return render_template("home.html")

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
        users[email] = {'password': password, 'description': '', 'photo': None, 'hobbies': [], 'likes_received': [], 'matches': []}
        session["user"] = email
        return redirect(url_for('edit_profile'))
    else:
        return render_template("index.html", error=_('Користувач з такою поштою вже існує.'), form_to_show='register')

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session: return redirect('/')
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
        return redirect(url_for('find_matches'))
    return render_template('edit_profile.html', user=users[email], hobbies_list=HOBBIES)

@app.route('/find_matches')
def find_matches():
    if 'user' not in session: return redirect('/')
    current_user_email = session['user']
    
    if 'match_queue' not in session or not session['match_queue']:
        current_user_hobbies = set(users[current_user_email].get('hobbies', []))
        
        # Exclude users already liked or matched
        seen_users = set(g.user_data['likes_received']) | set(g.user_data['matches'])
        
        potential_matches = []
        for email, profile in users.items():
            if email == current_user_email or email in seen_users:
                continue
            user_hobbies = set(profile.get('hobbies', []))
            if current_user_hobbies.intersection(user_hobbies):
                potential_matches.append(email)
        
        random.shuffle(potential_matches)
        session['match_queue'] = potential_matches

    if session['match_queue']:
        next_candidate_email = session['match_queue'].pop(0)
        session.modified = True
        candidate_profile = users.get(next_candidate_email)
        return render_template('find_matches.html', candidate=candidate_profile, email=next_candidate_email)
    else:
        return render_template('find_matches.html', candidate=None)

@app.route('/like/<string:liked_email>')
def like(liked_email):
    if 'user' not in session: return redirect('/')
    current_user_email = session['user']

    # Check for mutual like
    if current_user_email in users[liked_email]['likes_received']:
        # It's a match!
        users[current_user_email]['matches'].append(liked_email)
        users[liked_email]['matches'].append(current_user_email)
        
        # Clean up likes_received lists
        users[liked_email]['likes_received'].remove(current_user_email)
        if liked_email in users[current_user_email]['likes_received']:
             users[current_user_email]['likes_received'].remove(liked_email)

        return redirect(url_for('new_match', matched_email=liked_email))
    else:
        # One-way like, add to the liked user's list
        if current_user_email not in users[liked_email]['likes_received']:
            users[liked_email]['likes_received'].append(current_user_email)

    # If the like came from the notifications page, redirect there
    if 'notifications' in request.referrer:
        return redirect(url_for('notifications'))
        
    return redirect(url_for('find_matches'))

@app.route('/swap/<string:swapped_email>')
def swap(swapped_email):
    if 'user' not in session: return redirect('/')
    
    # If the swap came from the notifications page, remove the like
    if 'notifications' in request.referrer:
        if swapped_email in g.user_data['likes_received']:
            g.user_data['likes_received'].remove(swapped_email)
        return redirect(url_for('notifications'))

    return redirect(url_for('find_matches'))

@app.route('/notifications')
def notifications():
    if 'user' not in session: return redirect('/')
    
    likers_emails = g.user_data.get('likes_received', [])
    likers_profiles = {email: users[email] for email in likers_emails}
    
    return render_template('notifications.html', likers=likers_profiles)

@app.route('/my_matches')
def my_matches():
    if 'user' not in session: return redirect('/')
    
    matches_emails = g.user_data.get('matches', [])
    matches_profiles = {email: users[email] for email in matches_emails}
    
    return render_template('my_matches.html', matches=matches_profiles)

@app.route('/new_match/<string:matched_email>')
def new_match(matched_email):
    if 'user' not in session: return redirect('/')
    
    match_profile = users.get(matched_email)
    return render_template('new_match.html', match=match_profile, match_email=matched_email)

@app.route('/chat/<string:chat_with_email>')
def chat(chat_with_email):
    if 'user' not in session: return redirect('/')
    
    # Check if they are actually a match
    if chat_with_email not in g.user_data.get('matches', []):
        return redirect(url_for('home')) # Or show an error
        
    chat_partner = users.get(chat_with_email)
    return render_template('chat.html', partner=chat_partner, partner_email=chat_with_email)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)