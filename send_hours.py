from flask import Blueprint, render_template, request, session, flash, redirect
from DB import DB
import datetimeHelp
from Employee import Employee
from Shift import Shift
from datetime import date as dt


sendHoursBP = Blueprint("send_hours", __name__, static_folder="static", template_folder="templates")

db = DB("Resty.db")
@sendHoursBP.route("/send_hours", methods=["POST", "GET"])
# get after user chooses group
def send_hours():
    """
    Employee sends work hours request form
    :return:
    """
    try:
        if request.method == "POST":

            # match the user's days request
            user_id = request.form["user_id"]
            dates = request.form["dates"] # convert days to date - accepted format YYYY-MM-DD  HH:MM
            start_time = request.form["hours"]
            end_time = "NULL"
            # change arrangement and employee logic to handle multiple hour choice,
            for date in dates:
                db.insert_employee_times(user_id, date, start_time, end_time)

            flash("Shift options recorded successfully")
            return redirect("/send_hours")
            # session.pop('_flashes', None)
            # flash("Attendance failed to register")

        if request.method == "GET":
            org_id = 1  # get user's org_id
            start_date = datetimeHelp.next_weekday(dt.today(),6)  # next week's Sunday
            end_date = datetimeHelp.next_weekday(dt.today(), 12)  # next week's Saturday
            raw_shifts = db.get_shifts_by_date_range(org_id, start_date, end_date)
            shifts = [Shift(shift[0], shift[1], shift[2]) for shift in raw_shifts]
            return render_template("send_hours.html", params={"shifts":shifts})

        else:
            return render_template("error_page.html")

    except IOError:
        print("Error")


if __name__ == "__main__":

    e1 = Employee(1, 1, {"bartender": 1}, ["01-01-2020", "07-01-2020", "03-01-2020"])
    e2 = Employee(2, 2, {"waitress": 1}, ["01-01-2020", "02-01-2020", "04-01-2020", "07-01-2020"])
    e3 = Employee(3, 3, {"bartender": 1}, ["01-01-2020", "02-01-2020", "03-01-2020", "07-01-2020"])
    e4 = Employee(4, 4, {"bartender": 1}, ["02-01-2020", "04-01-2020", "05-01-2020", "06-01-2020"])
    e5 = Employee(5, 5, {"waitress": 2, "bartender": 1},
                  ["02-01-2020", "03-01-2020"])  # remove 3-1-20 to get best non viable solution
    e6 = Employee(6, 6, {"waitress": 1, "bartender": 1}, ["01-01-2020", "06-01-2020", "05-01-2020"])
    e7 = Employee(7, 7, {"waitress": 1}, ["01-01-2020", "07-01-2020", "05-01-2020"])
    e8 = Employee(8, 8, {"waitress": 1, "bartender": 1}, ["06-01-2020", "05-01-2020"])
    e9 = Employee(9, 9, {"waitress": 1}, ["03-01-2020", "04-01-2020", "06-01-2020"])
    e10 = Employee(10, 10, {"bartender": 1, "waitress": 1}, ["01-01-2020", "02-01-2020", "04-01-2020", "07-01-2020"])
    db = DB("Resty.db")
    for employee in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]:
        dates = employee.get_dates()
        user_id = employee.get_id()
        start_time = None
        for date in dates:
            date ="\"{}\"".format(datetimeHelp.swap_date_format(date))  # fix formatting to insert date to DB
            db.insert_employee_times(user_id, date, start_time)
    print(datetimeHelp.next_weekday(dt.today(),6))  # date of next sunday
    print(datetimeHelp.next_weekday(dt.today(),12))