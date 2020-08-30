from flask import Blueprint, render_template, request, session, flash, redirect

loginBP = Blueprint("login", __name__, static_folder="static", template_folder="templates")
from DB import DB

db = DB("Resty.db")


@loginBP.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    else:
        return render_template("error_page.html")


