from flask import Blueprint, render_template, request

arrangementBP = Blueprint("arrangement", __name__, static_folder="static", template_folder="templates")

@arrangementBP.route("/arrangement", methods=["GET"])
def arrangement():
    if request.method == "GET":
        return render_template("arrangement.html")

    else:
        return render_template("error_page.html")


if __name__ == "__main__":
    pass
