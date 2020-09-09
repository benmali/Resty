from flask import Blueprint, render_template, request, session
import json
from DB import DB
from classes.Employee import Employee
from classes.WorkWeek import WorkWeek
from classes.WorkDay import WorkDay
from classes.Shift import Shift
from classes.Matrix import Matrix

arrangementInfoBP = Blueprint("arrangement_info", __name__, static_folder="static", template_folder="templates")


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
        employees = Employee.create_from_DB(raw_employees)
        raw_shifts = db.get_shifts_by_date_range(org_id, start_date, end_date)
        shifts = Shift.create_from_DB(raw_shifts)
        raw_workdays = db.get_wdays_by_date_range(org_id, start_date, end_date)
        workdays = WorkDay.create_from_DB(org_id, raw_workdays)

        # add shifts to corresponding days
        for shift in shifts:
            for i in range(len(workdays)):
                if shift.get_date() == workdays[i].get_date():
                    workdays[i].add_shift(shift)

        ww = WorkWeek(workdays)
        dic, sol = ww.create_arrangement(employees, same_day_scheduling)
        employees, shifts = ww.extract_solution(sol)
        mat = Matrix(employees, shifts)
        # dic is a dictionary that maps number of shifts assigned to a employee
        # sol is the actual solved arrangement
        # for example {1:[E1,E2], 2:[E3,E4]..}

        # add arrangement to DB
        # db.register_arrangement(sol, session["sol"])
        #print(WorkWeek.min_shifts_swap(dic,sol))
        # 2: [Employee 5, tom col, dict_keys(['waitress', 'bartender']), Employee 7, itzik shawarma, dict_keys(['waitress']), Employee 8, roni kofif, dict_keys(['waitress', 'bartender'])],
        # 3: [Employee 6, pagi pagi, dict_keys(['waitress', 'bartender']), Employee 4, niv mali, dict_keys(['bartender']), Employee 9, some guy, dict_keys(['waitress']), Employee 1, ben mali, dict_keys(['bartender']), Employee 2, paz mali, dict_keys(['waitress']), Employee 3, rom mali, dict_keys(['bartender'])],
        # 4: [Employee 10, another guy, dict_keys(['bartender', 'waitress'])], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}]

        #2: [Employee 5, tom col, dict_keys(['waitress', 'bartender']), Employee 7, itzik shawarma, dict_keys(['waitress']), Employee 8, roni kofif, dict_keys(['waitress', 'bartender'])],
        # 3: [Employee 6, pagi pagi, dict_keys(['waitress', 'bartender']), Employee 4, niv mali, dict_keys(['bartender']), Employee 9, some guy, dict_keys(['waitress']), Employee 1, ben mali, dict_keys(['bartender']), Employee 10, another guy, dict_keys(['bartender', 'waitress']), Employee 3, rom mali, dict_keys(['bartender'])],
        # 4: [Employee 2, paz mali, dict_keys(['waitress'])]
        #swap 2 and 10 set 10 to 4 min
        dic, solution = ww.min_shifts_swap(dic, sol)
        return json.dumps(sol)
    else:
        return render_template("error_page.html")


if __name__ == "__main__":
    user_id = 1  # get logged in user's ID
    org_id = db.get_org_by_usr(user_id)[0][0]  # get user org_id
    #raw_employees = db.get_employees_by_date_range(org_id, "1-1-2020", "7-1-2020")
    employees = Employee.create_from_DB(db.get_employees_by_date_range(org_id, "2020-01-01", "2020-01-07"))
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
