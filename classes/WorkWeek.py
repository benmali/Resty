from classes.Shift import Shift
from classes.WorkDay import WorkDay
from classes import datetimeHelp
from classes.Employee import Employee
import random
import copy
from classes.Matrix import Matrix
import itertools
from DB import DB


class WorkWeek:
    def __init__(self, work_days):
        """

        :param work_days: a list of work day objects
        """
        self.work_days = work_days

    @classmethod
    def from_template(cls, org_id, template_no):  # for future use
        """
        initialize WorkWeek from template
        :param org_id: Org id
        :param template_no: number of template in DB user chose
        :return: WorkWeek object
        """
        try:
            db = DB("Resty.db")
            templates = db.get_ww_templates(org_id)  # get all the templates
            templates_dic = {}
            for shift in templates:
                template = shift[-1]
                if template in templates_dic:
                    templates_dic[template] += [shift]
                else:
                    templates_dic[template] = [shift]
            if template_no in templates_dic:  # user requested an existing template
                chosen_template = templates_dic[template_no]
                dates = datetimeHelp.this_week_dates()  # next week dates
                workdays = {}
                workdays_lst = []
                for shift in chosen_template:
                    if shift[0] in workdays:
                        workdays[shift[0]] += [shift]
                        # create workday
                    else:
                        workdays[shift[0]] = [shift]
                print(workdays)
                shift_id = db.get_max_shift_id(org_id)[0] + 1
                for day, shifts in workdays.items():
                    date = datetimeHelp.day_to_date(day, dates)
                    shift_lst = [Shift(shift_id + i, date, shifts[i][1], shifts[i][2], shifts[i][3]) for i in
                                 range(len(shifts))]
                    shift_id += len(shifts)
                    wd = WorkDay(org_id, date)
                    wd.set_shifts(shift_lst)
                    workdays_lst.append(wd)
                return cls(workdays_lst)

            else:
                print("template doesn't exist")

            # create Workdays from data, add them together to create WW

        except IOError:
            print("Failed to create template from restore")

    def create_arrangement(self, employees, same_day_scheduling=False):
        """
        get needed shifts for each day
        for each shift find number of needed staff
        get random employee and fit him to shift
        add shift to employees

        """
        """"""

        def schedule():
            """
            try schedule a chosen employee to shift
            :return: True if successfully scheduled Employee to Shift, False else
            """
            if shift.get_date() in chosen_employee.get_dates().keys():
                if shift.get_start_hour() in chosen_employee.get_dates()[shift.get_date()]:
                    # makes sure employee isn't already scheduled to work
                    # same_day_scheduling is set to false by default
                    if chosen_employee not in day.get_employees() or same_day_scheduling:
                        if chosen_employee not in shift.get_employees():
                            chosen_employee.add_shift(shift)
                            shift_dic[i + 1] += [chosen_employee]
                            decrement_list = shift_dic[i]
                            decrement_list.remove(chosen_employee)
                            shift_dic[i] = decrement_list
                            day.add_employee(chosen_employee)
                            return True
            return False

        try:
            # same_day_scheduling is a variable that can be changed to enable same day scheduling
            # get number of employees in eligible date range
            # employees should be a dictionary, mapping between dates and available employees
            # create employee objects
            # limit the number of shifts an employee can have per week to 10
            # initialize dictionary where its' keys are number of shifts and values are list of employee ids which have
            # this number of shifts assigned
            # this method is good when you need even distribution between employees
            # create dictionary to map num of shifts per employee
            max_shifts = 10
            max_num_employees = 0  # the maximum number of scheduled employees so far
            required_employees = 0  # the number of scheduled employees needed for a full solution
            days = [day for day in self.work_days[:]]
            shifts = []
            best = []
            for day in days:
                for shift in day.get_shifts():
                    shifts.append(shift)
                    # sums up the needed number of employees to create full arrangement
                    required_employees += shift.get_num_barts() + shift.get_num_waits()

            for j in range(50):  # try to find solution 50 times
                num_employees = 0
                shift_dic = {0: employees[:]}  # reset dictionary if no solution was found
                [employee.reset_shifts() for employee in employees[:]]  # reset shifts for employees
                solution = []
                [day.reset_shifts() for day in self.work_days[:]]
                for i in range(1, max_shifts + 1):
                    shift_dic[i] = []
                for day in self.work_days:  # iterate over every day of the WordDay element
                    for shift in day.get_shifts():  # iterate over every shift in the WorkDay
                        num_bartenders = shift.get_num_barts()
                        num_waitresses = shift.get_num_waits()
                        num_scheduled_bartenders, num_scheduled_waitresses = 0, 0
                        for i in range(7):
                            if num_bartenders == num_scheduled_bartenders and num_waitresses == num_scheduled_waitresses:
                                break  # scheduling shift is over, break loop
                            if shift_dic[i]:
                                possible_employees = [bartender for bartender in shift_dic[i] if
                                                      "bartender" in bartender.get_positions()]
                            else:
                                continue
                            while num_bartenders > num_scheduled_bartenders:
                                if len(possible_employees) == 0:
                                    break
                                # try schedule the first strong employee found
                                if day.is_first_shift(shift) and not shift.get_bartenders():
                                    chosen_employee = Shift.get_senior_employee(shift.get_date(), "bartender", 2,
                                                                                possible_employees)
                                    # find a senior employee that can work at this shift
                                else:  # not the first shift of the day, fill randomly
                                    chosen_employee = random.choice(possible_employees)
                                if not chosen_employee:  # no match found for a senior employee
                                    # try schedule another employee instead, manager decision
                                    chosen_employee = random.choice(possible_employees)
                                if schedule():
                                    shift.add_bartender(chosen_employee)
                                    num_scheduled_bartenders += 1
                                    # remove chosen employee anyway, not viable for scheduling in this shift anymore
                                possible_employees.remove(chosen_employee)

                            possible_employees = [waitress for waitress in shift_dic[i] if
                                                  "waitress" in waitress.get_positions()]  # filter out waitresses from
                            while num_waitresses > num_scheduled_waitresses:
                                if len(possible_employees) == 0:  # if no possible match found
                                    break
                                if day.is_first_shift(
                                        shift) and not shift.get_waitresses():  # try schedule the first strong employee found
                                    chosen_employee = Shift.get_senior_employee(shift.get_date(), "waitress", 2,
                                                                                possible_employees)
                                else:  # not the first shift of the day, fill randomly
                                    chosen_employee = random.choice(possible_employees)
                                    # makes sure employee is able to work at this shift
                                if not chosen_employee:  # no match found for the employee
                                    chosen_employee = random.choice(possible_employees)
                                if schedule():
                                    shift.add_waitress(chosen_employee)
                                    num_scheduled_waitresses += 1
                                # remove chosen employee anyway, not viable for scheduling in this shift anymore
                                possible_employees.remove(chosen_employee)
                        # end of while loops
                        solution.append(copy.deepcopy(shift))
                    num_employees += len(day.get_employees())
                if max_num_employees < num_employees:  # current solution is better than previous best
                    max_num_employees = num_employees
                    best = solution[:]
                    best_dictionary = copy.deepcopy(shift_dic)
                    print("\"\"\"\"\"")
                    print(best)
                    print("\"\"\"\"\"")
                    print("iteration: {}".format(j))

                if required_employees == num_employees:  # full solution found
                    return shift_dic, best
            print("No viable solution found - getting our best solution!")
            return best_dictionary, best

        except OverflowError:
            print("Too many loops - program shutdown")
        except IndexError:
            print("Cant create scheduling, no valid options")

    def min_shifts_swap(self, dic, solution):
        def switch():
            # emp.get_shifts().append(shift)
            # employee.get_shifts().remove(shift)
            # shift_dic[employee.get_id()] -= 1
            # shift_dic[emp.get_id()] += 1
            # # switch shifts between employees
            # emp_shifts = emp.get_shifts().append(shift1).remove(shift2)
            # employee_shifts = employee.get_shifts.append(shift2).remove(shift1)
            # shift1.remove(employee).append(emp)
            # shif2.append(employee).remove(emp)
            # employee.get_shifts().remove(shift)
            pass

        def take():
            """
            shift_dic: counts the number of shifts per employee
            dic: maps number of shifts to Employee objects
            :return:
            """
            dic[shift_dic[employee.get_id()]].remove(employee)  # remove employee from shift counter
            dic[shift_dic[employee.get_id()] - 1].append(employee)  # add employee to shift counter
            dic[shift_dic[emp.get_id()]].remove(emp)
            dic[shift_dic[emp.get_id()] + 1].append(emp)
            shift_dic[employee.get_id()] -= 1
            shift_dic[emp.get_id()] += 1
            emp.get_shifts().append(shift)
            employee.get_shifts().remove(shift)
            if emp.get_min_shifts() == len(emp.get_shifts()):
                under.remove(emp)
            if employee.get_min_shifts == len(employee.get_shifts()):
                over.remove(employee)

        shift_dic = {}  # map employee_id :num_shits
        changes = False
        over, under, exact = [], [], []
        for num_shifts, employees in dic.items():
            for employee in employees:
                shift_dic[employee.get_id()] = num_shifts
                if employee.get_id() == 10:
                    employee.set_min_shifts(2)
                if employee.get_id() == 2:
                    employee.set_min_shifts(4)
                else:
                    employee.set_min_shifts(0)
                if employee.get_min_shifts() > num_shifts:
                    under.append(employee)
                if employee.get_min_shifts() < num_shifts:
                    over.append(employee)
                else:
                    exact.append(employee)
        print(shift_dic)
        if over and under:  # both lists not empty
            for employee in over:
                for shift in solution:
                    emp_in_shift = shift.get_employees()
                    if employee in emp_in_shift:
                        shift_date = shift.get_date()
                        start_hour = shift.get_start_hour()
                        for emp in under:
                            if shift_date in emp.get_dates().keys():
                                if start_hour in emp.get_dates()[shift_date]:
                                    if employee in shift.get_bartenders() and "bartender" in emp.get_positions():
                                        shift.get_bartenders().remove(employee)
                                        shift.get_bartenders().append(emp)
                                        take()
                                        print("switched {} for {}".format(employee, emp))
                                        changes = True
                                        break
                                    if employee in shift.get_waitresses() and "waitress" in emp.get_positions():
                                        shift.get_waitresses().remove(employee)
                                        shift.get_waitresses().append(emp)
                                        take()
                                        print("switched {} for {}".format(employee, emp))
                                        changes = True
                                        break
        # if under:  # no direct switch possible and still employees left in under
        #     dic, solution = self.switch3(over, under, exact, dic, solution)
        if not changes:
            print("No changes done")
        print(shift_dic)
        return dic, solution

    # def switch3(self, over, exact, employees, shifts):
    #     mat = Matrix(employees, shifts)
    #     for over_employee in over:
    #         working_dates = mat.get_employee_dates(over_employee.get_id(), "w")
    #         for target_date in working_dates:
    #             for exact_employee in exact:
    #                 exact_dates = mat.get_employee_dates(exact_employee.get_id(), "w")
    #                 if target_date in exact_dates:  # potential switch possible
    #                     shift = mat.get_shift(target_date)
    #                     if over_employee in shift.get_bartenders() and "bartender" in exact_employee.get_positions():
    #                         shift.get_bartenders().remove(employee)
    #                         shift.get_bartenders().append(emp)
    #                         take()
    #                         print("switched {} for {}".format(employee, emp))
    #                         changes = True
    #                         break
    #                     if over_employee in shift.get_waitresses() and "waitress" in exact_employee.get_positions():
    #                         shift.get_waitresses().remove(employee)
    #                         shift.get_waitresses().append(emp)

    # find a date under wants
    # get from table list of employees who work there
    # filter out exact employees
    # find common dates between the exacts and the overs  -  rows where mat[i][over]==mat[i][exact]
    # on every match - check if they work in the shift
    # if they both work there and in correct position switch them
    # switch over employee with exact employee on another common date they have
    # take under and over
    # build matrix of possible shift but didn't get?
    # for emp_over in over:
    #     for emp_exact in exact:
    #         for emp_under in under:
    #             over_index = map_employee[emp_over.get_id()]
    #             exact_index = map_employee[emp_exact.get_id()]
    #             under_index = map_employee[emp_under.get_id()]
    #             common_over_exact = [reverse_date_map[i] for i in range(len(mat)) if mat[i][over_index]==mat[i][exact_index]]
    #             common_under_exact = [reverse_date_map[i] for i in range(len(mat)) if mat[i][under_index]==mat[i][exact_index]]

    # switch_shift(exact,over,shift)
    # take_shift(under,over,shift)
    # under wants exact's date, so switch exact problematic date to any common date he has with over
    # now over has the desired date
    # under takes the desired date from over

    # switch exact and over
    # take() with under and over

    # find employee with exact num_shifts, one with over number of shifts another with under
    # switch over and exact
    # switch over and under
    # exact
    # under_date -> find match with exact -> find match with over
    # if match found, rotate

    def extract_solution(self, solution):
        shifts, employees = [], []
        for shift in solution:
            for employee in shift.get_employees():
                if employee not in employees:
                    employees.append(employee)
            shifts.append(shift)
        return employees, shifts

    def create_combinations(self, employees):
        for employee in employees:
            for date in employee.get_dates():
                pass
    # lst = list(itertools.combinations(iterable, r))


if __name__ == "__main__":
    db = DB("Resty.db")
    # --- test 2 ----#
    s1 = Shift(1, "1-1-2020", "16:00")
    s2 = Shift(2, "1-1-2020", "19:00")
    s3 = Shift(3, "2-1-2020", "16:00")
    s4 = Shift(4, "2-1-2020", "19:00")
    s5 = Shift(5, "3-1-2020", "16:00")
    s6 = Shift(6, "3-1-2020", "19:00")
    s7 = Shift(7, "4-1-2020", "16:00")
    s8 = Shift(8, "4-1-2020", "19:00")
    s9 = Shift(9, "5-1-2020", "16:00")
    s10 = Shift(10, "5-1-2020", "19:00")
    s11 = Shift(11, "6-1-2020", "16:00")
    s12 = Shift(12, "6-1-2020", "19:00")
    s13 = Shift(13, "7-1-2020", "16:00")
    s14 = Shift(14, "7-1-2020", "19:00")
    wd = WorkDay("1-1-2020", "16:00", "Tom")
    wd2 = WorkDay("2-1-2020", "16:00", "Tom")
    wd3 = WorkDay("3-1-2020", "16:00", "Tom")
    wd4 = WorkDay("4-1-2020", "16:00", "Tom")
    wd5 = WorkDay("5-1-2020", "16:00", "Tom")
    wd6 = WorkDay("6-1-2020", "16:00", "Tom")
    wd7 = WorkDay("7-1-2020", "16:00", "Tom")
    wd.add_shift(s1)
    wd.add_shift(s2)
    wd2.add_shift(s3)
    wd2.add_shift(s4)
    wd3.add_shift(s5)
    wd3.add_shift(s6)
    wd4.add_shift(s7)
    wd4.add_shift(s8)
    wd5.add_shift(s9)
    wd5.add_shift(s10)
    wd6.add_shift(s11)
    wd6.add_shift(s12)
    wd7.add_shift(s13)
    wd7.add_shift(s14)
    ww = WorkWeek([wd, wd2, wd3, wd4, wd5, wd6, wd7])
    shifts = Shift.create_from_DB(db.get_shifts_by_date_range(1, "2020-01-01", "2020-01-07"))
    employees = Employee.create_from_DB(db.get_employees_by_date_range(1, "2020-01-01", "2020-01-07"))
    mat = Matrix(shifts, employees)  # get employees and shifts AFTER initial solution~

    print(employees)
    print("sd")
    # db.register_arrangement(sol)
