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
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")