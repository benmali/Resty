from flask import Flask, url_for, redirect, render_template, session,flash
from register import registerBP
app = Flask(__name__)

#bp of main - get
#bp register employee - post + get
#bp show arrangement - get
#bp create arrangment - get/post
#bp login - post/get
app.register_blueprint(registerBP, url_prefix="")

if __name__ == "__main__":
    app.run(debug=True)