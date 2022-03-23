from bottle import default_app, get, post, request, response, run, static_file, view
import uuid
import g
import time
import re
from datetime import datetime

##############################
import login_get        # GET
import explore_get      # GET
import logout_get       # GET

import signup_post      # POST
import login_post       # POST
import logout_post      # POST
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
# @get("/<user_handle>")
# @get("/<language>/<user_handle>")
# @view("user")
# def _(user_handle = "user_handle", language = "en"):
#     try:
#         if f"{language}_server_error" not in g.ERRORS: language = "en"

#         print("#"*30)
#         print(user_handle)
#         display_user = {}

#         for user in g.users:
#             if user_handle == user["user_handle"]:
#                 display_user = user

#         print("#"*30)
#         print(display_user)

#         return dict(user=display_user)
#     except Exception as ex:
#         print(ex)
#         return g._SEND(500, g.ERRORS[f"{language}_server_error"])

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")