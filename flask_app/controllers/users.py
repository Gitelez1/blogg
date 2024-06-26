from flask_app import app
from flask_app.models.user import User
from flask_app.models.blogg import Blogg
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def camperPage():
    return render_template("blogger.html")


@app.route("/")
def controller():
    if "user_id" not in session:
        return redirect("/logout")
    return redirect("/bloggs")


@app.route("/register")
def registerPage():
    if "user_id" in session:
        return redirect("/")
    return render_template("register.html")


@app.route("/login")
def loginpage():
    if "user_id" in session:
        return redirect("/")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginUser():
    if "user_id" in session:
        return redirect("/")
    user = User.get_user_by_email(request.form)
    if not user:
        flash("This user does not exist! Check your email.", "emailLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id']=user['id']
    return redirect('/bloggs')


@app.route("/register", methods=["POST"])
def register_user():
    if "user_id" in session:
        return redirect("/")
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash("This user already exists! Try another email.", "emailRegister")
        return redirect(request.referrer)

    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/bloggs")


@app.route("/bloggs")
def dashboardPage():
    if "user_id" not in session:
        return redirect("/")
    bloggs = Blogg.get_all_Bloggs()
    data = {"id": session['user_id']}
    loggeduser= User.get_user_by_id(data)
    return render_template("dashboard.html", bloggs=bloggs, loggeduser=loggeduser)



@app.route("/profile/<int:id>")
def profile(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    user =User.get_user_by_id(data)
    data2={
        'id':session['user_id']
    }
    loggeduser= User.get_user_by_id(data2)
    return render_template("profile.html", user=user, loggeduser=loggeduser)


@app.route("/edit/user")
def edit():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session['user_id']}
    user = User.get_user_by_id(data)
    return render_template("editProfile.html", user=user)


@app.route("/update/user", methods=["POST"])
def updateUser():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id'],
        "username": request.form["username"],
        "email": request.form["email"],
    }
    User.update_user(data)
    return redirect("/profile/" + str(session['user_id']))


@app.route("/delete")
def delete():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session['user_id']}
    Blogg.delete_users_blogg(data)
    User.delete_user(data)
    return redirect("/logout")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


