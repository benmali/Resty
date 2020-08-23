from flask import Blueprint, render_template, request, session, flash, redirect

arrangementBP = Blueprint("arrangement", __name__, static_folder="static", template_folder="templates")
from DB import DB
from Employee import Employee
from WorkWeek import WorkWeek
from WorkDay import WorkDay
from Shift import Shift
import datetimeHelp
db = DB("Resty.db")


@arrangementBP.route("/arrangement", methods=["GET"])
def arrangement():
    if request.method == "GET":
        user_id = 1  # get logged in user's ID
        org_id = db.get_org_by_usr(user_id)[0][0]  # get user org_id
        raw_employees = db.get_employees_by_date_range(org_id, "1-1-2020", "7-1-2020")
        employee_dates = {}  # map e_id to dates
        employee_names = {}
        employees = []
        for employee in raw_employees:
            e_id = employee[0]
            if e_id in employee_dates:
                employee_dates[e_id] += [employee[3]]
            else:
                employee_dates[e_id] = [employee[3]]
            if e_id not in employee_names:
                employee_names[e_id] = employee[1] + " " + employee[2]
        for e_id in employee_dates.keys():
            positions = db.get_employee_positions(e_id)
            positions_dic = {}
            for position in positions:
                positions_dic[position[0]] = position[1]
            employees.append(Employee(e_id, employee_names[e_id], positions_dic, employee_dates[e_id]))
        raw_shifts = db.get_shifts_by_date_range(org_id, "1-1-2020", "7-1-2020")
        shifts = [Shift(shift[0], datetimeHelp.swap_date_format(shift[1]), shift[2]) for shift in raw_shifts]
        raw_workdays = db.get_wdays_by_date_range(org_id, "1-1-2020", "7-1-2020")
        workdays = [WorkDay(org_id, wd[0], wd[1]) for wd in raw_workdays]
        ww = WorkWeek(workdays)
        dic, sol = ww.create_arrangement(org_id, "1-1-2020", "7-1-2020", employees)
        # pass solution to Front End, build as JS table
        return render_template("arrangement.html")


if __name__ == "__main__":
    user_id = 1  # get logged in user's ID
    org_id = db.get_org_by_usr(user_id)[0][0]  # get user org_id
    raw_employees = db.get_employees_by_date_range(org_id, "1-1-2020", "7-1-2020")
    employee_dates = {}  # map e_id to dates
    employee_names = {}
    employees = []
    for employee in raw_employees:
        e_id = employee[0]
        if e_id in employee_dates:
            employee_dates[e_id] += [employee[3]]
        else:
            employee_dates[e_id] = [employee[3]]
        if e_id not in employee_names:
            employee_names[e_id] = employee[1] + " " + employee[2]
    for e_id in employee_dates.keys():
        positions = db.get_employee_positions(e_id)
        positions_dic ={}
        for position in positions:
            positions_dic[position[0]] = position[1]
        employees.append(Employee(e_id,employee_names[e_id],positions_dic,employee_dates[e_id]))
    raw_shifts = db.get_shifts_by_date_range(org_id, "1-1-2020", "7-1-2020")
    shifts = [Shift(shift[0],shift[1],shift[2]) for shift in raw_shifts]
    raw_workdays = db.get_wdays_by_date_range(org_id, "1-1-2020", "7-1-2020")
    workdays = [WorkDay(org_id, wd[0], wd[1]) for wd in raw_workdays]
    i=0
    # add shifts to corresponding days
    for shift in shifts:
        while i < len(workdays):
            if shift.get_date() == workdays[i].get_date():
                workdays[i].add_shift(shift)
                break
            else:
                i+=1



    ww = WorkWeek(workdays)
    dic, sol = ww.create_arrangement(org_id, "01-01-2020", "07-01-2020", employees)
    for shift in sol:
        print(shift)
    print(dic)
    #print(employees)