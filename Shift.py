
import datetimeHelp
from datetime import date as dt
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

    def __repr__(self):
        return "shift id: {}, date: {}, bartenders: {}, waitresses: {}".format(self.shift_id,
                                                                               self.date,
                                                                               self.bartenders,
                                                                               self.waitresses)

    @classmethod
    def create_templates(cls, org_id):
        """
        Create a dictionary template_no: list of shifts
        :param org_id:
        :return:
        """
        db = DB("Resty.db")
        templates = db.get_ww_templates(org_id)  # get all the templates
        templates_dic = {}
        for shift in templates:
            template = shift[-1]
            if template in templates_dic:
                templates_dic[template] += [shift]
            else:
                templates_dic[template] = [shift]
        return templates_dic

    @classmethod
    def create_from_template(cls, org_id, template_no):
        """
        Create shifts based on template and insert to DB
        :return:
        """
        try:
            db = DB("Resty.db")
            templates_dic = Shift.create_templates(org_id)
            if template_no in templates_dic:  # user requested an existing template
                chosen_template = templates_dic[template_no]
                dates = [str(datetimeHelp.next_weekday(dt.today(), i)) for i in range(6, 13)]  # next week dates
                workdays = {}
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
                    date = "\"{}\"".format(date)
                    for i in range(len(shifts)):
                        shift_id+=i
                        start_hour ="\"{}\"".format(shifts[i][1])
                        db.insert_shift(org_id, shift_id, start_hour, date, shifts[i][2], shifts[i][3])
                    shift_id += 1
        except IOError:
            print("IO Error")

    def create_employee(self):
        """
        create Employee from data
        :return:
        """
        pass

    def is_full(self):
        return len(self.bartenders) == self.num_bartenders and len(self.waitresses) == self.num_waitresses

    def reset_shift(self):
        self.bartenders = []
        self.waitresses = []

    def get_num_barts(self):
        return self.num_bartenders

    def get_num_waits(self):
        return self.num_waitresses

    def get_day(self):
        """
        :return: String day name - "Monday"
        """
        day = datetimeHelp.convert_to_date(self.date)
        return day.strftime("%A")

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
    first_shift = Shift(1,"2020-01-01","16:00")
    print(first_shift.get_day())
    db = DB("Resty.db")
    data = db.get_employees()
    Shift.create_from_template(1, 1)
