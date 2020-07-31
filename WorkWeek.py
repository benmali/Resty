from Shift import Shift
from WorkDay import WorkDay
from Employee import Employee
from DB import DB


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
    def calculate_salaries(employees):
        total = 0
        for employee in employees:
            total += employee.calculate_salary()
        return total

    @staticmethod
    def create_arrangement():
        """
        get needed shifts for each day
        for each shift find number of needed staff
        get random employee and fit him to shift
        add shift to employees
        """
        e1 = Employee(1,1,1,["bartender"])
        e2 = Employee(2,2,2,["waitress"])
        s1 = Shift("1-1-20","16:00")
        s2 = Shift("2-1-20","16:00")
