from bottle import default_app, get, post, request, response, run, static_file, view
import uuid
import g
import time
import re
from datetime import datetime

##############################
import tweet_post       # POST

##############################
@get("/scripts/<script>")
def _(script):
    return static_file(script, root="./scripts")

##############################
@get("/images/<image>")
def _(image):
    return static_file(image, root="./images", mimetype="image/*")

##############################
@get("/")
@view("index")
def _():
    return

##############################
@post("/signup")
@post("/<language>/signup")
def _(language = "en"):

    user_first_name, error = g._IS_NAME(request.forms.get("user_first_name"), language, "first")
    if error: return g._SEND(400, error)
    user_last_name, error = g._IS_NAME(request.forms.get("user_last_name"), language, "last")
    if error: return g._SEND(400, error)

    user = {
        "user_first_name": user_first_name,
        "user_last_name": user_last_name
    }

    return user

##############################
@get("/<user_handle>")
@get("/<language>/<user_handle>")
@view("user")
def _(user_handle, language = "en"):
    display_user = {}

    for user in g.users:
        if user_handle == user["user_handle"]:
            display_user = user

    print("#"*30)
    print(display_user)

    return dict(user_handle=user_handle, user=display_user)

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")