from bottle import default_app, get, post, request, response, run, static_file, view
import uuid
import g
import time
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

    return dict(user_handle=user_handle)

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")