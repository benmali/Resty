import datetime
"""
    strftime prints 
    %A - Full day of the week
    %d day of the month
    %B - full month name
    %m	Month as a number 01-12
    %Y full year
    %M full month
    %H	Hour 00-23
    %M	Minute 00-59
    %% prints %

    strptime conerts string to date

    date_str1 = 'Wednesday, June 6, 2018'
    date_str2 = '6/6/18'
    date_str3 = '06-06-2018'

    # Define dates as datetime objects
    date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')
    date_dt2 = datetime.strptime(date_str2, '%m/%d/%y')
    date_dt3 = datetime.strptime(date_str3, '%m-%d-%Y')
    """
def convert_to_str(date):
    """
    :param date: datetime object
    :return: string of date, Israel formatted
    """
    return date.strftime("%d-%m-%Y")

def get_day(date):
    return date.strftime("%A")

def convert_to_date(date_str):
    """
    :param date_str: string of date, Israel formatted
    :return: datetime object
    """
    new_date = list(map(int,date_str.split("-"))) # splits the string to day ,month,year
    return datetime.datetime(new_date[0],new_date[1],new_date[2])

if __name__ == "__main__":
    print(convert_to_date('09-11-18'))
    date = datetime.datetime(2018, 6, 1)
    print(convert_to_str(date))