from bottle import post, request, response
import uuid
import g
import time
from datetime import datetime

##############################
@post("/signup")
@post("/<language>/signup")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"

        # Validate
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
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db = g._DB_CONNECT("database.sqlite")
        db.execute("""
            INSERT INTO users
            VALUES(
                :user_id, 
                :user_first_name, 
                :user_last_name,
                :user_email,
                :user_handle, 
                :user_password,
                :user_image_src,
                :user_description,
                :user_created_at,
                :user_created_at_date,
                :user_updated_at,
                :user_updated_at_date
            )
        """, user)
        db.commit()
        response.status = 201
        return user
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()
    
    # Connect to the DB
    # Insert the user to the users table