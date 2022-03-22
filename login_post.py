from bottle import post, request, response
import g
import uuid
import time
import jwt

##############################
@post("/login")
@post("/<language>/login")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"

        user_email, error = g._IS_EMAIL(request.forms.get("user_email"), language)
        if error: return g._SEND(400, error)
        for user in g.users:
            if user["user_email"] == user_email:
                user_password, error = g._IS_PASSWORD(request.forms.get("user_password"), language)
                if error: return g._SEND(400, error)
                if not user["user_password"] == user_password:
                    errors = {
                        "en": "Password is incorrect.",
                        "da": "Kodeordet er ikke korrekt."
                    }
                    return g._SEND(400, errors[language])
                    
                # SUCCES
                user_session = {
                    "user_id": user["user_id"],
                    "session_id": str(uuid.uuid4),
                    "iat": int(time.time())
                }
                
                encoded_jwt = jwt.encode(user_session, g.JWT_SECRET, algorithm="HS256")
                response.set_cookie("jwt", encoded_jwt)

                return  g._SEND(200, "Succesfull log in.")
        errors = {
            "en": "Email does not match a user.",
            "da": "Email er ikke tilknyttet en bruger."
        }
        return g._SEND(400, errors[language])

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])