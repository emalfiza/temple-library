import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo  # To get Flask interacting with MongoDB #
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "temple_library"
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_book")
def get_book():
    """
    Route to the Home page
    """
    return render_template("index.html", book=mongo.db.book.find())


@app.route("/add_book")
def add_book():
    """
    add_book function returns collections to view for filters on the home page
    """
    return render_template("addbook.html")


@app.route("/insert_book", methods=["POST"])
def insert_book():
    """
    After the add_book.html form filled and has been submited
    this route is called to insert the book to the database.
    """
    book = mongo.db.book
    book.insert_one(request.form.to_dict())
    return redirect(url_for("get_book"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
