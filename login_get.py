from bottle import get, view, redirect, request
import g
import jwt

##############################
@get("/login")
@get("/<language>/login")
@view("login")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    cookie = request.get_cookie("jwt")
    print(cookie)
    if cookie is not None:
        return redirect("/explore")

    return
