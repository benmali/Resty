from Shift import Shift
from WorkDay import WorkDay
from Employee import Employee
import random
from DB import DB


class WorkWeek:
    def __init__(self, work_days):
        """

        :param work_days: a list of work day objects
        """
        self.work_days = work_days

    @staticmethod
    def calculate_salaries(employees):
        total = 0
        for employee in employees:
            total += employee.calculate_salary()
        return total

    def create_arrangement(self, start_date, end_date, employees = None):
        """
        get needed shifts for each day
        for each shift find number of needed staff
        get random employee and fit him to shift
        add shift to employees
        """
        try:
            db = DB("Resty.db")
            # get number of employees in eligible date range
            #employees = db.get_employees_by_date_range("1-1-2020", "4-1-2020")
            # employees should be a dictionary, mapping between dates and available employees
            bartenders = [bartender for bartender in employees if "bartender" in bartender.get_positions()]
            waitresses = [waitress for waitress in employees if "waitress" in waitress.get_positions()]

            # create employee objects
            # limit the number of shifts an employee can have per week to 10
            max_shifts = 10
            # initialize dictionary where its' keys are number of shifts and values are list of employee ids which have
            # this number of shifts assigned
            # this method is good when you need even distribution between employees
            shift_dic = {0: employees}
            # create dictionary to map num of shifts per employee
            for i in range(1, max_shifts + 1):
                shift_dic[i] = []
            for day in self.work_days:  # iterate over every day of the WordDay element
                for shift in day.get_shifts():  # iterate over every shift in the WorkDay
                    num_bartenders = shift.get_num_barts()
                    num_scheduled_bartenders = 0
                    num_waitresses = shift.get_num_waits()
                    num_scheduled_waitresses = 0
                    for i in range(7):
                        if num_bartenders == num_scheduled_bartenders:
                            break  # scheduling shift is over, break look
                        if shift_dic[i] is not None:
                            possible_employees = [bartender for bartender in shift_dic[i] if
                                              "bartender" in bartender.get_positions()]
                        else:
                            continue
                        while num_bartenders > num_scheduled_bartenders:
                            # filter out bartenders from all employees

                            if len(possible_employees) ==0: # if no possible match found
                                continue
                            else:
                                chosen_employee = random.choice(possible_employees)
                                if shift.get_date() in chosen_employee.get_dates():
                                    shift.add_bartender(chosen_employee)
                                    chosen_employee.add_shift(shift.get_shift_id())
                                    increment_list = shift_dic[i+1]
                                    increment_list.append(chosen_employee)
                                    shift_dic[i+1] = increment_list
                                    decrement_list = shift_dic[i]
                                    decrement_list.remove(chosen_employee)
                                    shift_dic[i] = decrement_list
                                    num_scheduled_bartenders+=1
                                else: # employee cant work at this date
                                    possible_employees.remove(chosen_employee)
                    for i in range(7):
                        if num_waitresses == num_scheduled_waitresses:
                            print(shift)
                            break  # scheduling shift is over, break look
                        if shift_dic[i] is not None:
                            possible_employees = [waitress for waitress in shift_dic[i] if
                                                  "waitress" in waitress.get_positions()]   # filter out waitresses from
                        else:
                            continue
                        while num_waitresses > num_scheduled_waitresses:

                            if len(possible_employees) == 0:  # if no possible match found
                                continue
                            else:
                                chosen_employee = random.choice(possible_employees)
                                if shift.get_date() in chosen_employee.get_dates():
                                    shift.add_waitress(chosen_employee)
                                    chosen_employee.add_shift(shift.get_shift_id())
                                    increment_list = shift_dic[i + 1]
                                    increment_list.append(chosen_employee)
                                    shift_dic[i + 1] = increment_list
                                    decrement_list = shift_dic[i]
                                    decrement_list.remove(chosen_employee)
                                    shift_dic[i] = decrement_list
                                    num_scheduled_waitresses+=1
                                else:  # employee cant work at this date
                                    possible_employees.remove(chosen_employee)
            return shift_dic

        except OverflowError:
            print("Too many loops - program shutdown")
        except IndexError:
            print("Cant create scheduling, no valid options")


if __name__ == "__main__":

    s1 = Shift(1, "1-1-2020", "16:00")
    s2 = Shift(2, "2-1-2020", "16:00")
    #s3 = Shift(3, "2-1-2020", "19:00")
    wd = WorkDay("1-1-2020","16:00","Tom")
    #protect against inserting shifts with diffrent date than day to workday
    # to do - return error on specific day with no solution, make program skip it
    wd.add_shift(s1)
    wd2 = WorkDay("2-1-2020", "16:00", "Tom")
    wd2.add_shift(s2)
    #wd2.add_shift(s3)
    wd3 = WorkDay("4-1-20","16:00","Tom")
    e1 = Employee(1, 1, {"bartender": 1},["1-1-2020"])
    e2 = Employee(2, 2, {"waitress": 1}, ["2-1-2020"])
    e3 = Employee(3, 3, {"bartender": 1},["1-1-2020","2-1-2020"])
    e4 = Employee(4, 4, {"bartender": 1}, ["2-1-2020"])
    e5 = Employee(5, 5, {"waitress": 2, "bartender": 1},["2-1-2020"])
    e6 = Employee(6, 6, {"waitress": 1}, ["1-1-2020"])
    ww = WorkWeek([wd, wd2])
    #ww.create_arrangement("1-1-2020","4-1-2020",[e1,e2,e3,e4,e5,e6])
    #print(s1,s2)
    print(ww.create_arrangement("1-1-2020","4-1-2020",[e1,e2,e3,e4,e5,e6]))
    # test case without e6 to see what happens when script cant complete scheduling