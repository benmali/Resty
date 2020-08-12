from Employee import Employee
from datetimeHelp import convert_to_str, convert_to_date,get_day
import datetime
from DB import DB


class Shift:
    def __init__(self, shift_id, date, start_hour, num_bartenders=1, num_waitresses=1):
        """
        create a shift object with default number of employees
        this object is the shift to be scheduled
        :param date: date of shift
        :param start_hour: statring hour
        :param bartenders: list of Employees
        :param num_bartenders: int of needed Employees
        :param waitresses: list of Employee
        :param num_waitresses: int of needed Employee
        """
        self.shift_id = shift_id
        self.date = date
        self.start_hour = start_hour
        self.num_bartenders = num_bartenders
        self.num_waitresses = num_waitresses
        self.bartenders = []
        self.waitresses = []

    def create_employee(self):
        """
        create Employee from data
        :return:
        """
        pass

    def get_num_barts(self):
        return self.num_bartenders

    def get_num_waits(self):
        return self.num_waitresses

    def get_day(self):
        """
        :return: String day name - "Monday"
        """
        return get_day(self.date)

    def get_date(self):
        return self.date

    def get_shift_id(self):
        return self.shift_id

    def get_start_hour(self):
        return self.start_hour

    def add_bartender(self, bartender):
        self.bartenders.append(bartender)

    def add_waitress(self, waitress):
        self.waitresses.append(waitress)

    def update_tips(self):
        pass

    def get_bartenders(self):
        return self.bartenders

    def get_waitresses(self):
        return self.waitresses



class EmployeeShift:
    def __init__(self, shift, end_hour):
        """
        this is the shift object of a specific employee
        :param shift: shift object that the employee was scheduled in
        :param end_hour: actual ending hour
        """
        self.start_hour = shift.get_start_hour()
        self.date = shift.get_date()
        self.end_hour = end_hour
        self.employees = []

    def get_employees(self):
        return self.employees


@staticmethod
def get_employees_for_shift():
    """
    open DB
    get employees data
    return list of employees
    method to poll employees from DB
    :return: list of Employee objects
    """
    db = DB("Resty.db")
    bartenders = db.get_bartenders()
    waitresses = db.get_waitresses()
    for employee in data:
        pass

    return []
if __name__ == "__main__":
    # bart = Employee(1,2,3,4)
    # waiter = Employee(2,3,4,5)
    # date = datetime.datetime(20,6,15,16)
    # first_shift = Shift(date,date.hour,[bart], 1, [waiter], 1)
    db = DB("Resty.db")
    data = db.get_employees()

