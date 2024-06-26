from flask_app import app
from flask_app.models.blogg import Blogg
from flask_app.models.user import User
from flask import Flask, render_template, redirect, request, session, flash
import os
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename


#check if the formau is right
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/bloggs/new")
def addBlogg():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("addBlogg.html", loggeduser=loggeduser)


@app.route("/books")
def Books():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("books.html", loggeduser=loggeduser)

@app.route("/about")
def aboutAs():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("about.html", loggeduser=loggeduser)

@app.route("/emergency")
def emergency():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("emergency.html", loggeduser=loggeduser)

@app.route("/contact")
def contact():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("contact.html", loggeduser=loggeduser)


@app.route("/add/blogg", methods=["POST"])
def createBlogg():
    if "user_id" not in session:
        return redirect("/")
    if not Blogg.validate_blogg(request.form):
        return redirect(request.referrer)
    if not request.files['image']:
        flash('Show image is required!', 'image')
        return redirect(request.referrer)
    image = request.files['image']
    if not allowed_file(image.filename):
        flash('Image should be in png, jpg, jpeg format!', 'image')
        return redirect(request.referrer)
    if image and  allowed_file(image.filename):
        filename1 = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time+= filename1
        filename1 = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    data = {
        "description": request.form["description"],
        "image": filename1,
        "location": request.form["location"],
        'user_id': session['user_id']
    }
    Blogg.create(data)
    return redirect("/bloggs")


@app.route("/blogg/<int:id>")
def viewBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    loggeduser = User.get_user_by_id(data)
    usersWhoLiked = Blogg.get_users_who_liked(data)
    return render_template("blogg.html", blogg=blogg, loggeduser=loggeduser, usersWhoLiked=usersWhoLiked, numOfLikes=len(Blogg.get_users_who_liked(data)))


@app.route("/delete/blogg/<int:id>")
def deleteBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    loggeduser = User.get_user_by_id(data)
    if blogg["user_id"] == loggeduser["id"]:
        Blogg.delete_all_likes(data)
        Blogg.delete_blogg(data)
    return redirect("/bloggs")


@app.route("/blogg/edit/<int:id>")
def editBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    if not blogg:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if blogg['user_id'] != loggeduser['id']:
        return redirect('/')
    return render_template("editBlogg.html", blogg=blogg, loggeduser=loggeduser)


@app.route("/update/blogg/<int:id>", methods=["POST"])
def updateBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    if not blogg:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if blogg['user_id'] != loggeduser['id']:
        return redirect('/')
    if (
        len(request.form["description"]) < 1
        or len(request.form["location"]) < 1
    ):
        flash("All fields required", "allRequired")
        return redirect(request.referrer)
    updateData={
        'description': request.form['description'],
        'location': request.form['location'],
        'blogg_id':id
    }
    Blogg.update_blogg(updateData)
    return redirect('/blogg/'+ str(id))


@app.route('/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'blogg_id': id,
        'id': session['user_id']
    }
    usersWhoLiked = Blogg.get_users_who_liked(data)
    if session['user_id'] not in usersWhoLiked:
        Blogg.addLike(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'blogg_id': id,
        'id': session['user_id']
    }    
    Blogg.removeLike(data)
    return redirect(request.referrer)
