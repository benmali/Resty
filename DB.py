import sqlite3
import os
import re
import logging
from pathlib import Path




class DB:
    def __init__(self, name):
        self.name = name

    def get_connection_path(self):
        return str(Path(os.getcwd())) + "/" + self.name
    def check_for_db(self):
        path = str(Path(os.getcwd()).parent)
        if not os.path.isfile(path+"/"+self.name):
            return os.path.isfile(self.name)
        return True

    def create_db(self):
        try:
            if not self.check_for_db():
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """CREATE TABLE Employee
                            (
                              employee_id INT NOT NULL,
                              first_name VARCHAR(50) NOT NULL,
                              last_name VARCHAR(50) NOT NULL,
                              min_shifts INT NOT NULL,
                              PRIMARY KEY (employee_id)
                            );
                          """
                query2 = """
                            CREATE TABLE Employee_Times
                            (
                              employee_id INT NOT NULL,
                              date DATE NOT NULL,
                              start_time DATE NOT NULL,
                              end_time DATE,
                              PRIMARY KEY (date, employee_id, start_time)
                            );
                          """
                query3 = """
                            CREATE TABLE Shift
                            (
                              org_id INT NOT NULL,  
                              shift_id INT NOT NULL,
                              start_time DATE NOT NULL,
                              date DATE NOT NULL,
                              num_bartenders INT NOT NULL,
                              num_waitresses INT NOT NULL,
                              tip DOUBLE,
                              PRIMARY KEY (org_id,shift_id)
                            );
                            """
                query4 = """
                            CREATE TABLE Employees_in_Shift
                            (
                              shift_id INT NOT NULL,
                              employee_id INT NOT NULL,
                              solution INT NOT NULL,
                              PRIMARY KEY (employee_id, shift_id,solution)
                            );"""

                query5 = """
                            CREATE TABLE User
                            (
                                user_id INT NOT NULL,
                                first_name VARCHAR(50) NOT NULL,
                                last_name VARCHAR(50) NOT NULL,
                                phone VARCHAR(50),
                                password VARCHAR(50) NOT NULL,
                                PRIMARY KEY (user_id)
                                );"""
                query6 = """
                            CREATE TABLE Employee_Positions
                            (
                              employee_id INT NOT NULL,
                              position VARCHAR(50) NOT NULL,
                              seniority INT NOT NULL,
                              base_salary DOUBLE NOT NULL,
                              PRIMARY KEY (position, employee_id)
                            );"""
                query7 = """
                            CREATE TABLE WorkDay
                            (   
                                org_id INT NOT NULL,
                                date DATE NOT NULL,
                                manager VARCHAR(50),
                                PRIMARY KEY (org_id, date)
                            );"""
                query8 = """
                            CREATE TABLE Employee_Shift
                            (
                                employee_id INT NOT NULL,
                                date DATE NOT NULL,
                                start_hour DATE NOT NULL,
                                end_hour DATE NOT NULL,
                                PRIMARY KEY (employee_id, date)
                            );"""
                query9 = """
                            CREATE TABLE Organization
                            (
                                org_id INT NOT NULL,
                                org_name VARCAHR(50) NOT NULL,
                                PRIMARY KEY (org_id)
                            );"""

                query10 = """
                             CREATE TABLE User_in_Org
                             (
                             org_id INT NOT NULL,
                             user_id VARCAHR(50) NOT NULL,
                             PRIMARY KEY (org_id, user_id)
                             );"""
                query11="""
                           CREATE TABLE Week_Template
                           (
                           org_id INT NOT NULL,
                           day VARCHAR(50) NOT NULL,
                           start_hour DATE NOT NULL,
                           num_bartenders INT NOT NULL, 
                           num_waitresses INT NOT NULL,
                           template_no INT NOT NULL,
                           PRIMARY KEY (org_id, day,start_hour,num_bartenders,num_waitresses,template_no));"""


                crsr.execute(query)
                crsr.execute(query2)
                crsr.execute(query3)
                crsr.execute(query4)
                crsr.execute(query5)
                crsr.execute(query6)
                crsr.execute(query7)
                crsr.execute(query8)  # finished shifts
                crsr.execute(query9)
                crsr.execute(query10)
                crsr.execute(query11)
                connection.commit()
                connection.close()

            else:
                logging.log(1, "DB exists")
        except IOError:
            print("DB already exists")

    def insert_employee(self, employee_id, first_name, last_name, min_shifts):
        """
        insert Employee into the DB
        :param employee_id:
        :param first_name:
        :param last_name:
        :param min_shifts: minimum number of shifts for an employee per week
        :return: True if insert successfully False else
        """
        if not self.check_for_db():  # if DB doesn't exist create it
            self.create_db()
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        insret_query = """INSERT INTO Employee
                          VALUES ({}, {},{},{});""".format(employee_id, first_name, last_name, min_shifts)
        crsr.execute(insret_query)
        connection.commit()
        connection.close()

    def sol_exists(self, org_id):
        """
        find if there is already a solution, if there is
        return the max solution number
        :return: max solution number or None
        """
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        query = """SELECT MAX(solution)
                   FROM Employees_in_Shift EIS 
                   JOIN User_in_Org UIO ON EIS.employee_id=UIO.user_id
                   WHERE UIO.org_id={}""".format(org_id)
        crsr.execute(query)
        data = crsr.fetchone()
        connection.close()
        return data

    def user_exists(self, user_id):
        """
        find if user exists in DB
        :param user_id: int - id of the user
        :return: True if exists in DB False else
        """
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        query = """SELECT * FROM User WHERE user_id={}""".format(user_id)
        crsr.execute(query)
        data = crsr.fetchone()
        connection.close()
        if not data:
            return False
        return True

    def logged_shift_exists(self, employee_id, date):
        try:
            if self.check_for_db():
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT * FROM Employee_Shift WHERE employee_id={} AND date={}""".format(employee_id, date)
                crsr.execute(query)
                data = crsr.fetchone()
                connection.close()
                if not data:
                    return False
                return True
        except IOError:
            print("DB Error")

    def employee_time_exists(self,employee_id,date):
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        query = """SELECT * FROM Employee_Times WHERE employee_id={} AND date={}""".format(employee_id, date)
        crsr.execute(query)
        data = crsr.fetchone()
        connection.close()
        if not data:
            return False
        return True

    def log_shift(self, employee_id, date, start_hour, end_hour):
        """
        log done shifts into DB
        :param employee_id: ID of the employee
        :param date: date
        :param start_hour: start hour
        :param end_hour: end hour
        :return:
        """
        try:
            if not self.logged_shift_exists(employee_id,date):
                if not self.check_for_db():  # if DB doesn't exist create it
                    self.create_db()
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """INSERT INTO Employee_Shift VALUES ({},\"{}\",\"{}\",\"{}\")""".format(employee_id,date,start_hour,end_hour)
                crsr.execute(query)
                connection.commit()
                connection.close()
        except IOError:
            print("DB Error")


    def insert_employee_times(self,employee_id,date, start_time="NULL", end_time="NULL"):
        """
        insert the arrangement request by the Employee to DB, Employee_Times table
        :param employee_id:
        :param date:
        :param start_time:
        :param end_time:
        :return:
        """
        try:
            if not self.employee_time_exists(employee_id, date):
                if not self.check_for_db():  # if DB doesn't exist create it
                    self.create_db()
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                start_time="NULL"
                query = """INSERT INTO Employee_Times VALUES ({},{},{},{})""".format(employee_id, date, start_time, end_time)

                crsr.execute(query)
                connection.commit()
                connection.close()
                return True
            return False

        except IOError:
            print(" DBError")

    def insert_user(self, user_id, first_name, last_name, phone, pass_hash):
        """

        :param user_id: int
        :param first_name: string
        :param last_name: string
        :param phone: int
        :param pass_hash: string  - hash of password
        :return: True if success False else
        """
        if not self.check_for_db():  # if DB doesn't exist create it
            self.create_db()
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        if not self.user_exists(user_id):
            query = """INSERT INTO User VALUES ({},{},{},{},{})""".format(user_id, first_name, last_name, phone, pass_hash)
            crsr.execute(query)
            connection.commit()
            connection.close()
            return True
        return False

    def get_employees(self):
        try:
            if self.check_for_db():  # if DB doesn't exist create it
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = "SELECT * FROM Employee"
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("No DB exists")

    def get_employee_positions(self, employee_id):
        """
        gets positions of employee by id
        :return: list of employee positions with seniority
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT position,seniority
                           FROM Employee_Positions
                           WHERE employee_id={}""".format(employee_id)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data

        except IOError:
            print("IO Error")

    def get_bartenders(self):
        """
        method to get all bartenders
        :return: list of bartenders
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT E.employee_id, first_name, last_name, seniority 
                FROM Employee E JOIN Employee_Positions EP ON E.employee_id=EP.employee_id 
                WHERE position="bartender";"""
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get bartenders")

    def get_waitresses(self):
        try:
            connection = sqlite3.connect(self.name)
            crsr = connection.cursor()
            query = """SELECT E.employee_id, first_name, last_name, seniority 
            FROM Employee E JOIN Employee_Positions EP ON E.employee_id=EP.employee_id 
            WHERE position="waitress";"""
            crsr.execute(query)
            data = crsr.fetchall()
            connection.close()
            return data
        except IOError:
            print("Failed to get waitresses")

    def get_managers(self):
        try:
            if self.check_for_db():  # check for DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT E.employee_id, first_name, last_name, seniority 
                FROM Employee E JOIN Employee_Positions EP ON E.employee_id=EP.employee_id 
                WHERE position="manager";"""
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get managers")

    def insert_shift(self, org_id, shift_id, start_hour, date, num_bartenders, num_waitresses,tip=0):
        try:
            if self.check_for_db():  # check for DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """INSERT INTO Shift VALUES ({},{},{},{},{},{},{})""".format(org_id,
                                                                                  shift_id,
                                                                                  start_hour,
                                                                                  date,
                                                                                  num_bartenders,
                                                                                  num_waitresses,tip)
                crsr.execute(query)
                connection.commit()
                connection.close()
        except IOError:
            print("Failed to insert Shifts")

    def get_max_shift_id(self,org_id):
        try:
            if self.check_for_db():  # check for DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT MAX(shift_id)
                            FROM Shift
                            WHERE org_id={}""".format(org_id)
                crsr.execute(query)
                data= crsr.fetchone()
                connection.close()
                return data
        except IOError:
            print("Error")



    def get_ww_templates(self, org_id):
        try:
            if self.check_for_db():  # check for DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query="""SELECT WT.day,start_hour,num_bartenders,num_waitresses,template_no
                         FROM Week_Template WT
                         WHERE org_id={}
                         ORDER BY template_no""".format(org_id)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get template")
    def get_day_shifts(self, date):
        try:
            if self.check_for_db():  # check for DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT shift_id 
                        FROM Day_Shifts 
                        WHERE date={};""".format(date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get shifts")

    def get_employees_by_date_range(self, org_id, start_date, end_date):
        """
        method to get employees between eligible dates
        :param start_date:
        :param end_date:
        :return: list of employees with possible dates
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT E.employee_id, first_name, last_name, ET.date, ET.start_time,E.min_shifts
                            FROM Employee E 
                            JOIN Employee_Times ET ON E.employee_id=ET.employee_id 
                        JOIN User_in_Org UIO ON ET.employee_id=UIO.user_id
                        WHERE org_id={}
                        AND ET.date BETWEEN \"{}\" AND \"{}\"
                        ORDER BY E.employee_id,ET.date""".format(org_id,start_date, end_date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
            else:
                return None
        except IOError:
            print("Failed to get bartenders")

    def restore_solutions_by_date(self, org_id, start_date, end_date): # in use
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT S.shift_id,S.date, EIS.employee_id,E.first_name,E.last_name,solution
                           FROM Employees_in_Shift EIS
                           JOIN User_in_Org UIO ON EIS.employee_id=UIO.user_id
                           JOIN Shift S ON EIS.shift_id=S.shift_id
                           JOIN Employee E ON E.employee_id=UIO.user_id
                           WHERE S.date BETWEEN \"{}\" AND \"{}\" 
                           AND UIO.org_id={}
                           ORDER BY solution, S.shift_id """.format(start_date, end_date, org_id)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data

        except IOError:
            print("IO Error")


    def get_shifts_by_date_range(self, org_id, start_date, end_date): # in use
        """
        get shifts between given dates
        :return:
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT shift_id, S.date, start_time 
                            FROM Shift S
                            WHERE org_id={} AND 
                            S.date BETWEEN \"{}\" AND \"{}\" """.format(org_id, start_date, end_date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data

        except IOError:
            print("IO Error")

    def get_wdays_by_date_range(self, org_id, start_date, end_date): # in use
        """
        get shifts between given dates
        :return:
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT WD.date, manager
                            FROM WorkDay WD
                            WHERE org_id={} AND
                            WD.date BETWEEN \"{}\" AND \"{}\" """.format(org_id, start_date, end_date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data

        except IOError:
            print("IO Error")

    def get_employee_shifts(self, employee_id):
        """
        :returns list of shift ids for specific employee
        :param employee_id:
        :return:
        """
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT shift_id
                            FROM Employee_Shift
                            WHERE employee_id={}};""".format(employee_id)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get bartenders")

    def register_arrangement(self, solution, sol_num=1):
        """
        register solution to DB (Employees_in_Shifts table)
        :param solution: list of solved shifts, containing Employee objects
        :param sol_num: int , indicates which to which solution scheduling option belongs to
        :return: None
        """
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        for shift in solution:
            shift_id = shift.get_shift_id()
            employees_in_shift = shift.get_bartenders() + shift.get_waitresses()
            for employee in employees_in_shift:
                e_id = employee.get_id()
                query = """ INSERT INTO Employees_in_Shift VALUES ({},{},{})""".format(shift_id, e_id,sol_num)
                crsr.execute(query)
        connection.commit()
        connection.close()

    def get_org_by_usr(self, user_id):
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        query =""" SELECT org_id
                   FROM User_in_Org
                   WHERE user_id={}""".format(user_id)
        crsr.execute(query)
        data = crsr.fetchall()
        connection.close()
        return data



if __name__ == "__main__":
    db = DB("Resty.db")
    db.create_db()
    #print(db.get_employees_by_date_range(100,"2020-01-01","2020-01-02"))
    print(db.restore_solutions_by_date(1,"2020-01-01","2020-01-07"))


    # print(db.get_bartenders())
    # print(db.get_employees())
    # print((db.get_waitresses()))
