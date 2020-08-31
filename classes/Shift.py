from classes import datetimeHelp

from datetime import date as dt
from DB import DB


class Shift:
    def __init__(self, shift_id, date, start_hour, num_bartenders=1, num_waitresses=1, seniority=0):
        """
        create a shift object with default number of employees
        this object is the shift to be scheduled
        :param date: date of shift
        :param start_hour: statring hour
        :param bartenders: list of Employees
        :param num_bartenders: int of needed Employees
        :param waitresses: list of Employee
        :param num_waitresses: int of needed Employee
        :param bartenders: represents in a scale of 0-3 (0 - New Employee, 1 - Average ,2 - Strong , 3 - Manager/Very Strong)
        """
        self.shift_id = shift_id
        self.date = date
        self.start_hour = start_hour
        self.num_bartenders = num_bartenders
        self.num_waitresses = num_waitresses
        self.bartenders = []
        self.waitresses = []
        self.seniority = seniority

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
        # sort shifts by day
        for template_no, shifts in templates_dic.items():
            templates_dic[template_no] = sorted(shifts, key=lambda x: datetimeHelp.day_to_n(x[0]))

        return templates_dic

    @classmethod
    def get_senior_employee(cls, date, position, seniority, employees):
        """
        get a list of employees and a required position and a seniority lvl
        return the first employee that matches the criteria
        :param position: name of the postion
        :param seniority: seniority lvl 0-3
        :param date: date in YYYY-MM-DD Format
        :param employees: list of Employee objects
        :return: Employee
        """
        for employee in employees:
            # loop through the positions dictionary of every employee in the list
            for pos, sen in employee.get_positions().items():
                # if the lvl of seniority is more or equal to the requested
                # employee can work in a certain date, as well as senior enough
                if position == pos and sen >= seniority and date in employee.get_dates():
                    return employee

    @classmethod
    def create_from_DB(cls, raw_shifts):
        return [Shift(shift[0], shift[1], shift[2]) for shift in raw_shifts]

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
                shifts_lst = []
                for shift in chosen_template:
                    if shift[0] in workdays:
                        workdays[shift[0]] += [shift]
                        # create workday
                    else:
                        workdays[shift[0]] = [shift]
                print(workdays)
                for day, shifts in workdays.items():
                    date = datetimeHelp.day_to_date(day, dates)
                    date = "\"{}\"".format(date)
                    for i in range(len(shifts)):
                        start_hour = "\"{}\"".format(shifts[i][1])  # add quotes to start hour for DB
                        shifts_lst.append((org_id, start_hour, date, shifts[i][2], shifts[i][3]))
                # templates are pre-sorted in create_templates()
                # insert to DB as they are
                shift_id = db.get_max_shift_id(org_id)[0] + 1
                [db.insert_shift(shifts_lst[i][0], shift_id + i, shifts_lst[i][1], shifts_lst[i][2], shifts_lst[i][3],
                                 shifts_lst[i][4], 0) for i in range(len(shifts_lst))]
        except IOError:
            print("IO Error")

    def create_employee(self):
        """
        create Employee from data
        :return:
        """
        pass

    def get_seniority(self):
        return self.seniority

    def set_seniority(self, seniority):
        self.seniority = seniority

    def require_seniority(self, position):
        if position == "bartender":
            return self.bar_seniority != 0

        if position == "waitress":
            return self.wait_seniority != 0

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

    def get_employees(self):
        return self.bartenders+ self.waitresses


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
    first_shift = Shift(1, "2020-01-01", "16:00")
    print(first_shift.get_day())
    db = DB("Resty.db")
    data = db.get_employees()
    Shift.create_from_template(1, 1)
