from bottle import get, view, request
import g

##############################
@get("/login")
@get("/<language>/login")
@view("login")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    errors = {
        "en": False,
        "da": False
    }
    form_error = request.params.get("error")
    user_email = request.params.get("user_email")

    if form_error == "user_not_found": 
        errors = {
            "en": "The user does not exist.",
            "da": "Brugeren findes ikke."
        }
    if form_error == "incorrect_password":
        errors = {
            "en": "The password was incorrect.",
            "da": "Kodeordet var inkorrekt."
        }

    return dict(error=errors[language], user_email=user_email)
