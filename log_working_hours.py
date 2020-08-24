from flask import Blueprint, render_template, request, session, flash, redirect

log_workBP = Blueprint("log_work", __name__, static_folder="static", template_folder="templates")
from DB import DB

db = DB("Resty.db")


@log_workBP.route("/log_work", methods=["GET"])
def log_work():
    if request.method == "GET":
        return render_template("log_work.html")



    else:
        return render_template("error_page.html")

