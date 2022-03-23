from bottle import get, view, redirect, request
import g
import jwt

##############################
@get("/logout")
@get("/<language>/logout")
@view("logout")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    cookie = request.get_cookie("jwt")
    print("#"*30)
    print(cookie)
    if cookie == None:
        return redirect("/login")

    return
