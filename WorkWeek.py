class WorkWeek:
    def __init__(self, shifts):
        self.shifts = shifts

    def calculate_daily_tips(self, day, tips):
        """
        :param day: is a number between 1-7
        :param tips: total tips for the day
        :return: list of lists, with employee_id and tip
        """
        for shift in self.shifts:
            if shift.get_day() == day:
                pass
                # pull employees for specific day
                # sum all  work hours of employees
                #assign tip to employee - (work hours/total hours) * tips


@staticmethod
def calculate_salary(employees):
        for employee in employees:
            pass
