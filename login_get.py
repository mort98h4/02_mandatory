from bottle import get, view, request
import g

##############################
@get("/login")
@get("/<language>/login")
@view("login")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"
    return
