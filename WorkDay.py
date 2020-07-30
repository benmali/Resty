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


if __name__ == "__main__":
    pass