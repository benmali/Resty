class WorkWeek:
    def __init__(self, work_days):
        self.work_days = work_days

    def calculate_daily_tips(self, work_day, tips):
        """
        :param work_day:
        :param day: is a number between 1-7
        :param tips: total tips for the day
        :return: list of lists, with employee_id and tip
        """
        for shift in work_day:
            if shift.get_day() == work_day:
                pass
                # pull employees for specific day
                # sum all  work hours of employees
                #assign tip to employee - (work hours/total hours) * tips


@staticmethod
def calculate_salary(employees):
        for employee in employees:
            pass
