from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = []

@app.route("/")
def home():
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        users.append(name)
        return redirect("/")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)