from flask import Flask
from backend.register import registerBP
from backend.send_hours import sendHoursBP
from backend.main_page import mainBP
from backend.arrangement import arrangementBP
from backend.login import loginBP
from backend.log_working_hours import log_workBP
from backend.restore_shifts import restore_shiftsBP
from backend.week_templates import week_templatesBP
from backend.template_info import templates_infoBP
from backend.send_hours_info import sendHoursInfoBP
from backend.arrangement_info import arrangementInfoBP
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
app.register_blueprint(week_templatesBP, url_prefix="")
app.register_blueprint(templates_infoBP, url_prefix="")
app.register_blueprint(sendHoursInfoBP, url_prefix="")
app.register_blueprint(arrangementInfoBP, url_prefix="")
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