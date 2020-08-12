import datetime


class WorkDay:
    def __init__(self, date, start_hour, manager, end_hour=None):
        """
        :param date: datetime object
        :param start_hour: datetime object
        :param end_hour: datetime object
        :param shifts: list of Shift objects
        """
        self.date = date
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.manager = manager
        self.shifts = []

    def add_shift(self, shift):
        """
        add Shift object to shifts list
        :param shift:
        :return:None
        """
        self.shifts.append(shift)

    def calculate_daily_tips(self, work_day, tips):
        """
        :param work_day:
        :param day: is a number between 1-7
        :param tips: total tips for the day
        :return: list of lists, with employee_id and tip
        """
        for shift in self.shifts:
            if shift.get_day() == work_day:
                pass
                # pull employees for specific day
                # sum all  work hours of employees
                #assign tip to employee - (work hours/total hours) * tips

    def get_shifts(self):
        return self.shifts

if __name__ == "__main__":
    pass