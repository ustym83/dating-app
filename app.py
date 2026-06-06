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
        return "Неправильна пошта або пароль. <a href='/'>Повернутися</a>", 400

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if email and password:
        if email not in users:
            users[email] = password
            session["user"] = email
            return redirect("/")
        else:
            return "Користувач з такою поштою вже існує. <a href='/'>Повернутися</a>", 400
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)