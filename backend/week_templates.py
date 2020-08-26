from flask import Blueprint, render_template, request, session, flash, redirect
import json
week_templatesBP = Blueprint("templates", __name__, static_folder="static", template_folder="templates")
from classes.DB import DB
from classes.Shift import Shift

db = DB("Resty.db")


@week_templatesBP.route("/templates", methods=["GET"])
def templates():
    if request.method == "GET":
        org_id = 1
        templates = Shift.create_templates(1)
        json_templates = json.dumps(templates)

        return render_template("templates.html",params={"templates":templates,"json":json_templates})

    if request.method == "POST":
        org_id = 1 # get from user
        chosen_template = 1 # get from user
        Shift.create_from_template(org_id, chosen_template)  # create shifts in DB
