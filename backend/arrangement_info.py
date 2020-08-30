from flask import Blueprint, render_template, request, session, flash, redirect

arrangementInfoBP = Blueprint("arrangement_info", __name__, static_folder="static", template_folder="templates")
from DB import DB
from classes.Employee import Employee
from classes.WorkWeek import WorkWeek
from classes.WorkDay import WorkDay
from classes.Shift import Shift

db = DB("Resty.db")


@arrangementInfoBP.route("/arrangement_info", methods=["GET"])
def arrangement_info():
    if request.method == "GET":
        # make sure start_date is before end_date
        user_id = 1  # get logged in user's ID
        same_day_scheduling = False  # get this from user
        start_date = "1-1-2020"  # get this from user
        # start_date = str(datetimeHelp.next_weekday(dt.today(), 6)) - date of next Sunday
        end_date = "7-1-2020"  # get this from user
        # end_time = str(datetimeHelp.next_weekday(dt.today(), 12)) - date of next Saturday
        org_id = db.get_org_by_usr(user_id)[0][0]  # get user org_id
        sol_num = db.sol_exists(org_id)  # gets the max sol number from DB
        if sol_num[0]:  # if solution exists in DB
            session["sol"] = sol_num[0] + 1
        else:
            session["sol"] += 1
        raw_employees = db.get_employees_by_date_range(org_id, start_date, end_date)
        employees = Employee.employees_from_DB(raw_employees)
        raw_shifts = db.get_shifts_by_date_range(org_id, start_date, end_date)
        shifts = [Shift(shift[0], shift[1], shift[2]) for shift in raw_shifts]
        raw_workdays = db.get_wdays_by_date_range(org_id, start_date, end_date)
        workdays = [WorkDay(org_id, wd[0], wd[1]) for wd in raw_workdays]
        i = 0
        # add shifts to corresponding days
        for shift in shifts:
            while i < len(workdays):
                if shift.get_date() == workdays[i].get_date():
                    workdays[i].add_shift(shift)
                    break
                else:
                    i += 1

        ww = WorkWeek(workdays)
        dic, sol = ww.create_arrangement(employees, same_day_scheduling)
        # dic is a dictionary that maps number of shifts assigned to a employee
        # sol is the actual solved arrangement
        # for example {1:[E1,E2], 2:[E3,E4]..}

        # add arrangement to DB
        # db.register_arrangement(sol, session["sol"])
        return str([sol, dic])
    else:
        return render_template("error_page.html")


if __name__ == "__main__":
    user_id = 1  # get logged in user's ID
    org_id = db.get_org_by_usr(user_id)[0][0]  # get user org_id
    raw_employees = db.get_employees_by_date_range(org_id, "1-1-2020", "7-1-2020")
    employees = Employee.employees_from_DB(raw_employees)
    raw_shifts = db.get_shifts_by_date_range(org_id, "1-1-2020", "7-1-2020")
    shifts = [Shift(shift[0], shift[1], shift[2]) for shift in raw_shifts]
    raw_workdays = db.get_wdays_by_date_range(org_id, "1-1-2020", "7-1-2020")
    workdays = [WorkDay(org_id, wd[0], wd[1]) for wd in raw_workdays]
    i = 0
    # add shifts to corresponding days
    for shift in shifts:
        while i < len(workdays):
            if shift.get_date() == workdays[i].get_date():
                workdays[i].add_shift(shift)
                break
            else:
                i += 1
    ww = WorkWeek(workdays)
    dic, sol = ww.create_arrangement(employees)
    for shift in sol:
        print(shift)
    print(dic)
