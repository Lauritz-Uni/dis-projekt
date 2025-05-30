from flask import Blueprint, render_template

auth = Blueprint('auth', __name__) 

@auth.route('/login')
def login():
    user = "Isak"
    return render_template("login.html", text="testing", boolean=True, user=user)

@auth.route('/logout')
def logout():
    user = "Isak"
    return "<p>Logout</p>"

@auth.route('/sign-up')
def sign_up():
    user = "Isak"
    return render_template("sign_up.html", user=user)