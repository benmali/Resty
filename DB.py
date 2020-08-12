import sqlite3
import os
import re
import logging


class DB:
    def __init__(self, name):
        self.name = name

    def check_for_db(self):
        return os.path.isfile(self.name)

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
                              PRIMARY KEY (employee_id)
                            );
                          """
                query2 = """
                            CREATE TABLE Employee_Times
                            (
                              employee_id INT NOT NULL,
                              date INT NOT NULL,
                              start_time DATE,
                              end_time DATE,
                              PRIMARY KEY (date, employee_id)
                            );
                          """
                query3 = """
                            CREATE TABLE Shift
                            (
                              shift_id INT NOT NULL,
                              start_time DATE NOT NULL,
                              date DATE NOT NULL,
                              num_bartenders INT NOT NULL,
                              num_waitresses INT NOT NULL,
                              tip DOUBLE,
                              PRIMARY KEY (shift_id)
                            );
                            """
                query4 = """
                            CREATE TABLE Employees_in_Shift
                            (
                              employee_id INT NOT NULL,
                              shift_id INT NOT NULL,
                              PRIMARY KEY (employee_id, shift_id),
                              FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
                              FOREIGN KEY (shift_id) REFERENCES Shift(shift_id)
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
                              position VARCHAR(50) NOT NULL,
                              seniority INT NOT NULL,
                              employee_id INT NOT NULL,
                              base_salary DOUBLE NOT NULL,
                              PRIMARY KEY (position, employee_id)
                            );"""
                query7 = """
                            CREATE TABLE Day_Shifts
                            (
                                shift_id INT NOT NULL,
                                date DATE NOT NULL,
                                PRIMARY KEY (shift_id, date)
                            );"""
                query8 = """
                            CREATE TABLE Employee_Shift
                            (
                                employee_id INT NOT NULL,
                                shift_id INT NOT NULL,
                                start_hour DATE NOT NULL,
                                end_hour DATE NOT NULL,
                                date DATE NOT NULL,
                                PRIMARY KEY (shift_id, employee_id)
                                           );"""
                crsr.execute(query)
                crsr.execute(query2)
                crsr.execute(query3)
                crsr.execute(query4)
                crsr.execute(query5)
                crsr.execute(query6)
                crsr.execute(query7)
                crsr.execute(query8)  # finished shifts
                connection.commit()
                connection.close()

            else:
                logging.log(1, "DB exists")
        except IOError:
            print("DB already exists")

    def insert_employee(self):
        if not self.check_for_db():  # if DB doesn't exist create it
            self.create_db()
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        # insret_query = """INSERT INTO Resty.db (employee_id,product_name) VALUES ("{}", "{}");""".format(key, value)
        # crsr.execute(insret_query)
        # commit changes to DB
        connection.commit()
        # close the connection
        connection.close()

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

    def get_employee_options(self, start_date):
        try:
            if self.check_for_db():  # check fot DB existence
                connection = sqlite3.connect(self.name)
                crsr = connection.cursor()
                query = """SELECT E.employee_id, first_name, last_name, position, seniority 
                     FROM Employee E JOIN Employee_Positions EP ON E.employee_id=EP.employee_id 
                     JOIN Employee_Times ET ON E.employee_id=ET.employee_id
                     WHERE date={};""".format(start_date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get bartenders")

    def get_employees_by_date_range(self, start_date, end_date):
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
                query = """SELECT  E.employee_id, first_name, last_name, ET.position, ET.date
                        FROM Employee E JOIN Employee_Positions EP ON E.employee_id=EP.employee_id 
                        JOIN Employee_Times ET ON E.employee_id=ET.employee_id
                        WHERE ET.date BETWEEN {} AND {}};""".format(start_date,end_date)
                crsr.execute(query)
                data = crsr.fetchall()
                connection.close()
                return data
        except IOError:
            print("Failed to get bartenders")

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



if __name__ == "__main__":
    db = DB("Resty.db")
    db.create_db()
    # print(db.get_bartenders())
    # print(db.get_employees())
    # print((db.get_waitresses()))