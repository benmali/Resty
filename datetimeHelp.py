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


def swap_date_format(date):
    """
    flips the date format from or to YYYY-MM-DD
    :param date: string YYYY-MM-DD or DD-MM-YYYY
    :return:
    """
    return "-".join(date.split("-")[::-1])

def day_to_date(day, dates):
    """
    Convert Sunday to next Sunday's date etc.
    :param day: Sunday,Monday..
    :param dates: Corresponding date
    :return: date
    """
    switch = {
        "Sunday": dates[0],
        "Monday": dates[1],
        "Tuesday": dates[2],
        'Wednesday': dates[3],
        "Thursday": dates[4],
        "Friday": dates[5],
        "Saturday": dates[6]
    }
    return switch[day]

def compare_dates(date1, date2):
    """
    dates are YYYY-MM-DD formatted or YYYY-MM-DD HH:MM
    :param date1:
    :param date2:
    :return:
    """

    if len(date1) == len(date2):
        return date1==date2

    if len(date1)<len(date2):
        return date1==date2.split(" ")[0]
    else:
        return date2==date1.split(" ")[0]


def next_weekday(d, weekday):
    """
    # 0 = Monday, 1=Tuesday, 2=Wednesday...
    :param d:
    :param weekday:
    :return:
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)



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
    print(compare_dates("2020-01-02 16:00", "2020-01-01"))