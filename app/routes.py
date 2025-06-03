from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_dance.contrib.google import google
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Image, Comment
from flask import current_app as app

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("login.html")
    return redirect(url_for("main.dashboard"))

@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        file = request.files["image"]
        description = request.form["description"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            image = Image(filename=filename, description=description, user_id=current_user.id)
            db.session.add(image)
            db.session.commit()
            flash("Bild hochgeladen", "success")
    images = Image.query.all()
    return render_template("dashboard.html", images=images)

@main.route("/comment/<int:image_id>", methods=["POST"])
@login_required
def comment(image_id):
    text = request.form["comment"]
    new_comment = Comment(text=text, image_id=image_id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("main.dashboard"))

@main.route("/delete/<int:image_id>")
@login_required
def delete(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        flash("Du darfst nur deine eigenen Bilder löschen!", "danger")
        return redirect(url_for("main.dashboard"))
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(image)
    db.session.commit()
    flash("Bild gelöscht", "success")
    return redirect(url_for("main.dashboard"))

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
