class Employee:
    def __init__(self, e_id, name, positions, work_days=None, max_hours=None):
        """
        create an Employee object
        :param e_id: employee's ID
        :param name: employee's full name
        :param positions: dictionary containing position:seniority
        :param work_days: possible working days
        :param max_hours: set working hours limit
        """
        self.e_id = e_id
        self.name = name
        self.work_days = work_days
        self.max_hours = max_hours
        self.shifts = []
        self.scheduled_hours = 0
        self.positions = positions

    def __repr__(self):
        return "Employee {}, {}, {}".format(self.e_id, self.name, self.positions.keys())

    def add_shift(self, shift):
        self.shifts.append(shift)

    def set_shifts(self, shifts):
        self.shifts = shifts

    def get_position_names(self):
        return self.positions.keys()

    def get_positions(self):
        """
        get Employee positions
        :return: list of Positions
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

    def calculate_salary(self):
        for shift in self.shifts:
            pass

if __name__ == "__main__":
    pass
