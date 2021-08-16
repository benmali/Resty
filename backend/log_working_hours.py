from flask import Blueprint, render_template, request, session, flash, redirect

log_workBP = Blueprint("log_work", __name__, static_folder="static", template_folder="templates")
from classes.DB.DB import DB

db = DB("Resty.db")


@log_workBP.route("/log_work", methods=["GET","POST"])
def log_work():
    if request.method == "GET":
        return render_template("log_work.html")

    if request.method == "POST":
        user_id = 1 # get this from user
        start_hour = request.form["start_hour"]
        end_hour = request.form["end_hour"]
        date = request.form["date"]
        db.log_shift(user_id, date, start_hour, end_hour)
        return render_template("log_work.html")

    else:
        return render_template("error_page.html")


if __name__=="__main__":
    db.log_shift(1, "2020-01-08", "16:00", "23:00")