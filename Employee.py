class Employee:
    def __init__(self, e_id, name, seniority, positions, work_days=None, max_hours=None):
        self.e_id = e_id
        self.name = name
        self.seniority = seniority
        self.work_days = work_days
        self.max_hours = max_hours
        self.shifts = []
        self.scheduled_hours = 0
        self.positions = positions

    def add_shift(self, shift):
        self.shifts.append(shift)

    def hour_registration(self, shift, end_hour):
        """
        Employee will register working hours
        :param shift: Shift object
        :param end_hour: Shift end time
        :return: None
        """
        pass

    def calculate_salary(self):
        for shift in self.shifts:
            pass


