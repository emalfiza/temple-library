import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo  # To get Flask interacting with MongoDB #
from bson.objectid import ObjectId
from os import path

import urllib.request
import json

if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "temple_library"
app.config["MONGO_URI"] = os.getenv(
    "MONGO_URI", "mongodb://localhost:27017/db")

mongo = PyMongo(app)


@app.route("/about")
def about():
    """
    Route to about page
    """
    return render_template("about.html")


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


@app.route("/edit_book/<book_id>")
def edit_book(book_id):
    """
    This route renders the editbook.html page.
    """
    the_book = mongo.db.book.find_one({"_id": ObjectId(book_id)})
    return render_template("editbook.html", book=the_book)


@app.route("/update_book/<book_id>", methods=["POST"])
def update_book(book_id):
    book = mongo.db.book
    book.update({"_id": ObjectId(book_id)},
                {
        "book_name": request.form.get("book_name"),
        "book_writer": request.form.get("book_writer"),
        "book_genre": request.form.get("book_genre"),
        "book_cover": request.form.get("book_cover"),
        "description": request.form.get("description"),
    })
    return redirect(url_for('get_book'))


@app.route("/view_book/<book_id>")
def view_book(book_id):
    book_details = mongo.db.book.find_one({"_id": ObjectId(book_id)})
    return render_template("viewbook.html", book=book_details)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    mongo.db.book.remove({"_id": ObjectId(book_id)})
    return redirect(url_for("get_book"))


@app.route('/search_isbn', methods=['POST'])
def find_book_info():
    book_isbn = request.form['isbn'].strip()
    google_api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(google_api + book_isbn) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)
    return json.dumps(obj["items"][0])


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", 5000)),
            debug=True)
