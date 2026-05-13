from flask import Flask, render_template
from flask import request, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        post = Post(
            title=title,
            content=content
        )

        db.session.add(post)
        db.session.commit()

        return redirect("/")

    posts = Post.query.all()

    return render_template(
        "index.html",
        posts=posts
    )

@app.route("/delete/<int:id>")
def delete(id):

    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
