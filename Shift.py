from Employee import Employee
from datetimeHelp import convert_to_str, convert_to_date,get_day


class Shift:
    def __init__(self, date, start_hour, bartenders,num_bartenders, waitresses, num_waitresses ):
        """

        :param date: date of shift
        :param start_hour: statring hour
        :param bartenders: list of Employees
        :param num_bartenders: int of needed Employees
        :param waitresses: list of Employee
        :param num_waitresses: int of needed Employee
        """
        self.date = date
        self.start_hour = start_hour
        self.num_bartenders = num_bartenders
        self.num_waitresses = num_waitresses
        self.bartenders = bartenders
        self.waitresses = waitresses

        self.employees = []

    def get_day(self):
        """
        :return: String day name - "Monday"
        """
        return get_day(self.date)

    def get_hours(self):
        return self.hours

    def schedule_employees(self, date_range):
        try:
            # query employees with relevant dates
            #create employees from data
            employees = [Employee(1,1,1,1,1)]
            for employee in employees:
                if self.num_employess > len(self.employees):
                    self.employees.append(employee)  # add employee to shift
                    employee.add_shift(self)
            if self.num_employess != len(self.employees):
                # end of scheduling process result in not enough employees for shift
                raise ValueError

        except ValueError:
            print("Not Enough employees to complete scheduling")


if __name__ == "__main__":
    pass

