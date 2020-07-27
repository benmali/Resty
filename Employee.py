class Employee:
    def __init__(self, e_id, name, seniority, work_days, max_hours=None):
        self.e_id = e_id
        self.name = name
        self.seniority = seniority
        self.work_days = work_days
        self.max_hours = max_hours
        self.shifts = []
        self.scheduled_hours = 0

    def add_shift(self, shift):
        self.shifts.append(shift)


@staticmethod
def create_from_data(data, day):
    """
    :param data:
    :param day:
    :return: return list of relevant employees
    """
    return []


        