from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Словник для зберігання користувачів: email -> password
users = {}

@app.route("/")
def home():
    # Передаємо список email-ів для відображення
    return render_template("index.html", users=list(users.keys()))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if email in users and users[email] == password:
        session["user"] = email
        return redirect("/")
    else:
        # Повертаємо шаблон з повідомленням про помилку та вказуємо, яку форму показати
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error="Неправильна пошта або пароль.",
                               form_to_show='login')

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error="Пошта та пароль не можуть бути порожніми.",
                               form_to_show='register')

    if email not in users:
        users[email] = password
        session["user"] = email
        return redirect("/")
    else:
        # Повертаємо шаблон з повідомленням про помилку та вказуємо, яку форму показати
        return render_template("index.html", 
                               users=list(users.keys()), 
                               error="Користувач з такою поштою вже існує.",
                               form_to_show='register')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)