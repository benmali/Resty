from classes.User import User
import re
from DB import DB
db = DB("Resty.db")


class Employee(User):
    def __init__(self, e_id, name, positions, work_days=None, max_hours=None):
        """
        create an Employee object
        :param e_id: employee's ID
        :param name: employee's full name
        :param positions: dictionary containing position:seniority
        :param work_days: possible working days: start_hour dictionary
        :param max_hours: set working hours limit
        """
        self.e_id = e_id
        self.name = name
        self.work_days = {}

        for day in work_days:  # MUST BE IN #YYYY-MM-DD HH:MM format !
            date, time = day.split(" ")  # YYYY-MM-DD HH:MM format
            # ensure correct date formatting
            assert bool(re.match(r'20[2-9][0-9]-[0-1][1-9]-[0-3][1-9][0-2][0-9]:[0-5][0-9]', date + time)),\
                "Bad Hour Format"
            if date in self.work_days:
                self.work_days[date] += [time]
            else:
                self.work_days[date] = [time]

        self.max_hours = max_hours
        self.shifts = []
        self.scheduled_hours = 0
        self.positions = positions

    def __repr__(self):
        return "Employee {}, {}, {}".format(self.e_id, self.name, self.positions.keys())


    @classmethod
    def create_from_DB(cls, raw_employees):
        employee_dates, employee_names = {}, {}  # map e_id to dates
        employees = []
        for employee in raw_employees:
            e_id = employee[0]
            if e_id in employee_dates:
                if employee[4]:  # Employee request a specific time a his shift, combine date and hour
                    employee_dates[e_id] += [employee[3] + " " + employee[4]]
                else:
                    employee_dates[e_id] += [employee[3]]
            else:
                if employee[4]:
                    employee_dates[e_id] = [employee[3] + " " + employee[4]]
                else:
                    employee_dates[e_id] = [employee[3]]
            if e_id not in employee_names:  # combine first and last name
                employee_names[e_id] = employee[1] + " " + employee[2]
        for e_id in employee_dates.keys():
            positions = db.get_employee_positions(e_id)
            positions_dic = {}
            for position in positions:
                positions_dic[position[0]] = position[1]
            employees.append(Employee(e_id, employee_names[e_id], positions_dic, employee_dates[e_id]))
        return employees

    def get_full_name(self):
        name = self.name.split(" ")
        return name[0], name[1]

    def add_shift(self, shift):
        self.shifts.append(shift)

    def reset_shifts(self):
        self.shifts = []

    def set_shifts(self, shifts):
        self.shifts = shifts

    def get_position_names(self):
        return self.positions.keys()

    def get_positions(self):
        """
        get Employee positions
        :return: dictionary of Positions
        """
        return self.positions

    def get_dates(self):
        return self.work_days

    def hour_registration(self, shift, end_hour):
        """
        Employee will register working hours
        :param shift: Shift object
        :param end_hour: Shift end time
        :return: None
        """
        pass

    def get_id(self):
        return self.e_id

    @staticmethod
    def calculate_salaries(employees):
        total = 0
        for employee in employees:
            total += employee.calculate_salary()
        return total


if __name__ == "__main__":
    raw = db.get_employees_by_date_range(1,"2020-01-01","2020-01-07")
    emp = Employee.create_from_DB(raw)
    print(emp)
