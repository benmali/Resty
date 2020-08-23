from flask import Flask, session
from register import registerBP
from send_hours import sendHoursBP
from main_page import mainBP
from arrangement import arrangementBP
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
app.secret_key = "sxchahsdiu324wdasd"


if __name__ == "__main__":
    app.run(debug=True)