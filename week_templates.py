from flask import Blueprint, render_template, request, session, flash, redirect

week_templatesBP = Blueprint("templates", __name__, static_folder="static", template_folder="templates")
from DB import DB
from Employee import Employee
from WorkWeek import WorkWeek
from WorkDay import WorkDay
from Shift import Shift

db = DB("Resty.db")


@week_templatesBP.route("/templates", methods=["GET"])
def templates():
    if request.method == "POST":
        org_id = 1
        templates = Shift.create_templates(1)
        return render_template("templates.html",params={"templates":templates})

    if request.method == "POST":
        org_id = 1 # get from user
        chosen_template = 1 # get from user
        Shift.create_from_template(org_id, chosen_template)  # create shifts in DB
