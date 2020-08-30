from flask import Blueprint, flash, request, redirect
from classes import datetimeHelp
from classes.Shift import Shift
from datetime import date as dt
from DB import DB
import json

db = DB("Resty.db")
sendHoursInfoBP = Blueprint("send_hours_info", __name__, static_folder="static", template_folder="templates")


@sendHoursInfoBP.route("/send_hours_info", methods=["POST", "GET"])
def send_hours_info():
    try:
        if request.method == "GET":
            org_id = 1  # get user's org_id
            start_date = datetimeHelp.next_weekday(dt.today(), 6)  # next week's Sunday
            end_date = datetimeHelp.next_weekday(dt.today(), 12)  # next week's Saturday
            raw_shifts = db.get_shifts_by_date_range(org_id, start_date, end_date)
            shifts = [Shift(shift[0], shift[1], shift[2]) for shift in raw_shifts]
            return str([json.dumps(s.__dict__) for s in shifts])

        if request.method == "POST":
            # match the user's days request
            user_id = request.form["user_id"]
            dates = request.form["dates"]  # convert days to date - accepted format YYYY-MM-DD  HH:MM
            start_time = request.form["hours"]
            end_time = "NULL"
            # change arrangement and employee logic to handle multiple hour choice,
            for date in dates:
                db.insert_employee_times(user_id, date, start_time, end_time)

            flash("Shift options recorded successfully")
            return redirect("/send_hours")
            # session.pop('_flashes', None)
            # flash("Attendance failed to register")
    except IOError:
        print("Error fetching information")
