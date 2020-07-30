class Employee:
    def __init__(self, e_id, name, seniority, position, work_days=None, max_hours=None):
        self.e_id = e_id
        self.name = name
        self.seniority = seniority
        self.work_days = work_days
        self.max_hours = max_hours
        self.shifts = []
        self.scheduled_hours = 0
        self.position = position

    def add_shift(self, shift):
        self.shifts.append(shift)

    def hour_registration(self,shift,end_hour):
        """
        Employee will register working hours
        :param shift: Shift object
        :param end_hour: Shift end time
        :return: None
        """
        pass

@staticmethod
def create_from_data(data, day):
    """
    :param data:
    :param day:
    :return: return list of relevant employees
    """
    return Employee


        