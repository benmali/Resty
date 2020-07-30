from Employee import Employee

class Shift:
    def __init__(self, day, hours, num_employees):
        self.day = day
        self.hours = hours
        self.num_employess = num_employees
        self.employees = []

    def get_day(self):
        return self.day

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

