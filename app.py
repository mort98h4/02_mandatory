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
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"
        user_first_name, error = g._IS_NAME(request.forms.get("user_first_name"), language, "first")
        if error: return g._SEND(400, error)
        user_last_name, error = g._IS_NAME(request.forms.get("user_last_name"), language, "last")
        if error: return g._SEND(400, error)
        user_email, error = g._IS_EMAIL(request.forms.get("user_email"), language)
        if error: return g._SEND(400, error)
        user_email, error = g._ALREADY_EXISTS(user_email, "user_email", language)
        if error: return g._SEND(400, error)
        user_handle, error = g._IS_HANDLE(request.forms.get("user_handle"), language)
        if error: return g._SEND(400, error)
        user_handle, error = g._ALREADY_EXISTS(user_handle, "user_handle", language)
        if error: return g._SEND(400, error)
        user_password, error = g._IS_PASSWORD(request.forms.get("user_password"), language)
        if error: return g._SEND(400, error)

        if not request.forms.get("user_confirm_password"):
            errors = {
                "en":"Confirm password is missing.",
                "da":"Bekræft kodord mangler."
            }
            return g._SEND(400, errors[language])
        user_confirm_password = request.forms.get("user_confirm_password")
        if not user_confirm_password == user_password:
            errors = {
                "en":"Confirm password is not identical to password.",
                "da":"Bekræft kodeord er ikke identisk med kodeord."
            }
            return g._SEND(400, errors[language])

        user = {
            "user_id": str(uuid.uuid4()),
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_email": user_email,
            "user_handle": user_handle,
            "user_password": user_password,
            "user_image_src": "",
            "user_description": "",
            "user_created_at": str(int(time.time())),
            "user_created_at_date":datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"), 
            "user_updated_at":"", 
            "user_updated_at_date":""
        }
        response.status = 201
        return user
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])


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