from flask import Blueprint, render_template,request, session,flash
import hashlib
import DB
registerBP = Blueprint("register", __name__, static_folder="static", template_folder="templates")

@registerBP.route("/register",methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_id = request.form["user_id"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        password = request.form["password"]
        password_hash = hashlib.md5(password.encode()).hexdigest()
        db = DB("Resty.db")

        db.insert_user(user_id,first_name,last_name,phone,password_hash)

        return render_template("post_register.html")
    if request.method == "GET":
        return render_template("register.html")
