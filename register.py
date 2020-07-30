from flask import Blueprint, render_template,request, session,flash
registerBP = Blueprint("register", __name__, static_folder="static", template_folder="templates")

@registerBP.route("/register",methods=["POST", "GET"])
def register():
    if request.method == "POST":
        return render_template("post_register.html")
    if request.method == "GET":
        return render_template("register.html")
