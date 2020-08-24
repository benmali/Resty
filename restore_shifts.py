from flask import Blueprint, render_template, request, session, flash, redirect

restore_shiftsBP = Blueprint("restore_shifts", __name__, static_folder="static", template_folder="templates")
from DB import DB

db = DB("Resty.db")
@restore_shiftsBP.route("/restore_shifts", methods=["GET"])
def restore_shifts():
    if request.method == "GET":
        org_id=1
        start_date= "2020-01-01"
        end_date = "2020-01-07"
        data = db.restore_solutions_by_date(org_id,start_date,end_date)
        solutions = []
        sol = []
        current_sol = 1
        for i in range(len(data)):
            if data[i][5] == current_sol:
                sol.append(data[i])
            else:
                solutions.append(sol)
                sol = []
                sol.append(data[i])
                current_sol += 1
        solutions.append(sol)

        params = {"solutions":solutions}
        return render_template("restore_shifts.html",params=params)



if __name__=="__main__":
    db = DB("Resty.db")
    data = db.restore_solutions_by_date(1,"2020-01-01","2020-01-07")
    print(len(data))
    solutions = []
    sol = []
    max_sol_num = data[-1][5]
    current_sol = 1
    for i in range(len(data)):
        if data[i][5] == current_sol:
            sol.append(data[i])
        else:
            solutions.append(sol)
            sol = []
            sol.append(data[i])
            current_sol += 1
    solutions.append(sol)
    print(solutions)