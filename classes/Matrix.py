import numpy as np


class Matrix:
    def __init__(self, employees, shifts):
        """
        employees and shifts will be extracted from solution
        employees that didn't send work hours request will NOT be included here!
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
        :param map_shifts - map date to shift object
        :param jobs_mat - z axis layer of tensor
        """
        self.employees = employees
        self.shifts = shifts
        self.base_mat = np.zeros((len(self.shifts), len(self.employees)), dtype=int)
        self.employee_map = {}
        self.map_eid_employee = {}
        self.map_date_mat = {}
        self.map_eid_mat = {}
        self.map_shifts = {}
        self.reverse_mat_date = {}
        self.reverse_mat_eid = {}
        for i in range(len(shifts)):
            self.map_date_mat[shifts[i].get_full_time()] = i
            self.map_shifts[shifts[i].get_full_time()] = shifts[i]
        for j in range(len(employees)):
            self.map_eid_mat[employees[j].get_id()] = j
            self.employee_map[employees[j].get_id()] = employees[j]
        for key, value in self.map_date_mat.items():
            self.reverse_mat_date[value] = key
        for key, value in self.map_eid_mat.items():
            self.reverse_mat_eid[value] = key
        self.work_mat, self.jobs_mat = self.build_work_mat()
        self.tensor = np.array([self.work_mat, self.jobs_mat])
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
        build a 2nd matrix that represents which position an employee was scheduled to work at
        :return:
        """
        work_mat = np.copy(self.base_mat)
        jobs_mat = np.copy(self.base_mat)
        for employee in self.employees:
            for shift in employee.get_shifts():
                i = self.map_date_mat[shift.get_full_time()]
                j = self.map_eid_mat[employee.get_id()]
                work_mat[i][j] = 1
                if employee in shift.get_bartenders():
                    jobs_mat[i][j] = 1
                if employee in shift.get_waitresses():
                    jobs_mat[i][j] = 2
        return work_mat, jobs_mat

    def get_employee_dates(self, employee_id, mat_code):
        """
        get possible full dates for an employee from matrix
        "w" parameter will get working dates "r" will get requested dates, "o" will get requested but didn't get
        :param mat_code: "w" for work_mat ,"r" for request_mat, "o" for options_mat
        :param employee_id: employee id
        :return: dates that the employee requested/ works on/ can work and doesn't (depending on mat)
        """
        if mat_code == "w":
            mat = self.work_mat
        elif mat_code == "r":
            mat = self.request_mat
        else:
            mat = self.options_mat
        employee_key = self.map_eid_mat[employee_id]
        date_options = mat[:, employee_key]
        return [self.reverse_mat_date[i] for i in range(len(date_options)) if date_options[i] == 1]

    def get_employees_from_date(self, date, mat):
        """
        get possible employees on a specific date
        :param date: date to find employees that work in this day
        :param mat: work mat or request mat
        :return: employees that requested/working in specific date (depending on input mat)
        """
        date_key = mat[date]
        employee_options = mat[date_key, :]
        return [self.map_eid_employee[self.reverse_mat_eid[i]] for i in range(len(employee_options))
                if employee_options[i] == 1]

    def get_shift(self, date):
        """
        get shift object from date
        :param date: full date format YYYY:MM:DD HH:MM
        :return: Shift object
        """
        return self.map_shifts[date]

    def shift_job_matrix(self):
        """
        build upper layer of tensor
        might combine with other matrix methods (can unite them)
        :return:
        """
        mat = np.zeros(len(self.shifts), len(self.employees))
        for i in range(len(self.shifts)):
            for j in range(len(self.employees)):
                if self.employees[j] in self.shifts[i].get_bartenders():
                    mat[i][j] = 1
                elif self.employees[j] in self.shifts[i].get_waitresses():
                    mat[i][j] = 2
                else:
                    mat[i][j] = 0
        return mat


if __name__ == "__main__":
    work_mat = np.array([[1, 0, 1],
                         [0, 1, 1]])
    jobs_mat = np.array([[2, 0, 1],
                         [0, 2, 1]])
    tensor = np.array([work_mat, jobs_mat])
    print(tensor[1][0][0])
