from flask import Flask, session
from register import registerBP
from send_hours import sendHoursBP
from main_page import mainBP
from arrangement import arrangementBP
from login import loginBP
from log_working_hours import log_workBP
from restore_shifts import restore_shiftsBP
from week_templates import week_templatesBP
app = Flask(__name__)

#bp of main - get
#bp register employee - post + get
#bp show arrangement - get
#bp create arrangment - get/post
#bp login - post/get
#bp register to the website
app.register_blueprint(registerBP, url_prefix="")
app.register_blueprint(sendHoursBP, url_prefix="")
app.register_blueprint(mainBP, url_prefix="")
app.register_blueprint(arrangementBP, url_prefix="")
app.register_blueprint(loginBP, url_prefix="")
app.register_blueprint(log_workBP, url_prefix="")
app.register_blueprint(restore_shiftsBP, url_prefix="")
app.register_blueprint(week_templatesBP,rl_prefix="")
app.secret_key = "sxchahsdiusd324wdasd"
# run scheduled tasks
# import time
# import atexit
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run(debug=True)