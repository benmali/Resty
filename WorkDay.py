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


if __name__ == "__main__":
    pass