import numpy as np


class Matrix:
    def __init__(self, employees, shifts):
        """
        shifts = Shift.create_from_DB(db.get_shifts_by_date_range(org_id, start_date, end_date))
        employees = Employee.create_from_DB(db.get_employees_by_date_range(org_id, start_date, end_date))
        :param employees: list of Shift objects
        :param shifts: list of Employee objects
                 emp1, emp2, emp3, emp4
        date 1   1    1     0     0
        date 2   0    1     1     0
        date 3   0    0     0     1

        options_mat:
        0 will represent dates employee didn't request
        1 will represent dates employee asked for and didn't get
        2 will represent shifts he asked and got

        :param map_eid_employee - map employee_id: Employee object
        :param map_date_mat  - map date : mat_number
        :param map_eid_mat  - map employee_id : mat_number
        :param reverse_mat_date -  map mat index : date
        :param reverse_mat_eid - map mat index: employee_id
        """
        self.employees = employees
        self.shifts = shifts
        # self.base_mat = np.array([[0 for j in range(len(employees))] for i in range(len(shifts))])
        self.base_mat = np.zeros(len(self.shifts), len(self.employees))
        self.employee_map = {}
        self.map_eid_employee = {}
        self.map_date_mat = {}
        self.map_eid_mat = {}
        self.reverse_mat_date = {}
        self.reverse_mat_eid = {}
        for i in range(len(shifts)):
            self.map_date_mat[shifts[i].get_full_time()] = i
        for j in range(len(employees)):
            self.map_eid_mat[employees[j].get_id()] = j
            self.employee_map[employees[j].get_id()] = employees[j]
        for key, value in self.map_date_mat.items():
            self.reverse_mat_date[value] = key
        for key, value in self.map_eid_mat.items():
            self.reverse_mat_eid[value] = key
        self.work_mat = self.build_work_mat()
        self.request_mat = self.build_request_mat()
        self.options_mat = self.work_mat + self.request_mat

    def build_request_mat(self):
        """
        build matrix of possible shifts Employees can work in
        :return: np.array of requested shifts
        """
        request_mat = np.copy(self.base_mat)
        for employee in self.employees:
            for date in employee.get_full_date_lst():
                i = self.map_date_mat[date]
                j = self.map_eid_mat[employee.get_id()]
                request_mat[i][j] = 1
        return request_mat

    def build_work_mat(self):
        """
        build a matrix that represents shifts that employees work in
        :return:
        """
        work_mat = np.copy(self.base_mat)
        for employee in self.employees:
            for shift in employee.get_shifts():
                i = self.map_date_mat[shift.get_full_time()]
                j = self.map_eid_mat[employee.get_id()]
                work_mat[i][j] = 1
        return work_mat

    def get_employee_dates(self, employee_id, mat):
        """
        get possible full dates for an employee from matrix
        :param employee_id: employee id
        :param mat: work_mat or request_mat
        :return: dates that the employee requested/ works on (depending on mat)
        """
        employee_key = self.map_eid_mat[employee_id]
        date_options = mat[:, employee_key]
        return [self.reverse_mat_date[i] for i in range(len(date_options)) if date_options[i] == 1]

    def get_employees_from_date(self, date, mat):
        """
        get possible employees on a specific date
        :param date: date to find employees that work in this day
        :param mat: work mat or  request mat
        :return: employees that requested/working in specific date (depending on input mat)
        """
        date_key = mat[date]
        employee_options = mat[date_key, :]
        return [self.map_eid_employee[self.reverse_mat_eid[i]] for i in range(len(employee_options))
                if employee_options[i] == 1]
