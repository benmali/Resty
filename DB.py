import sqlite3
import os
import re


class DB:
    def __init__(self, name):
        self.name = name

    def check_for_db(self):
        return os.path.isfile(self.name)

    def create_db(self):
            connection = sqlite3.connect(self.name)
            crsr = connection.cursor()
            query = """CREATE TABLE Employee
                    (
                      employee_id INT NOT NULL,
                      fist_name VARCHAR(50) NOT NULL,
                      last_name VARCHAR(50) NOT NULL,
                      PRIMARY KEY (employee_id)
                    );
                    
                    CREATE TABLE Employee_Times
                    (
                      work_day INT NOT NULL,
                      start_time DATE NOT NULL,
                      end_time DATE NOT NULL,
                      employee_id INT NOT NULL,
                      PRIMARY KEY (work_day, employee_id),
                      FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
                    );
                    
                    CREATE TABLE Shift
                    (
                      shift_id INT NOT NULL,
                      work_day INT NOT NULL,
                      start_time DATE NOT NULL,
                      end_time DATE NOT NULL,
                      date DATE NOT NULL,
                      num_employees INT NOT NULL,
                      PRIMARY KEY (shift_id)
                    );
                    
                    CREATE TABLE Employees_in_Shift
                    (
                      employee_id INT NOT NULL,
                      shift_id INT NOT NULL,
                      PRIMARY KEY (employee_id, shift_id),
                      FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
                      FOREIGN KEY (shift_id) REFERENCES Shift(shift_id)
                    );"""
            crsr.execute(query)
            connection.commit()
            connection.close()

    def insert_employee(self):
        if not self.check_for_db():  # if DB doesn't exist create it
            self.create_db()
        connection = sqlite3.connect(self.name)
        crsr = connection.cursor()
        insret_query = """INSERT INTO Shufersal (product_id,product_name) VALUES ("{}", "{}");""".format(key, value)
        crsr.execute(insret_query)
        # commit changes to DB
        connection.commit()
        # close the connection
        connection.close()
