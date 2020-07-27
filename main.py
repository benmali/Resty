from flask import Flask, url_for, redirect, render_template, session,flash
app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True)