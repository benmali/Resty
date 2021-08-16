from flask import Blueprint, render_template, request, session, flash, redirect
import json
templates_infoBP = Blueprint("templates_info", __name__, static_folder="static", template_folder="templates")
from classes.DB.DB import DB
from classes.Shift import Shift

db = DB("Resty.db")

@templates_infoBP.route("/templates_info", methods=["GET"])
def templates_info():
    if request.method == "GET":
        org_id = 1  # get from user
        return json.dumps(Shift.create_templates(org_id))