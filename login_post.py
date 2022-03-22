from bottle import post, redirect, request, response
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
        user_password, error = g._IS_PASSWORD(request.forms.get("user_password"), language)
        if error: return g._SEND(400, error)

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        print("#"*30)
        print({"user_email": user_email, "user_password": user_password})

        db = g._DB_CONNECT("database.sqlite")
        user = db.execute(""" SELECT * FROM users
                              WHERE user_email = ?""", (user_email,)).fetchone()
        print(user)
        if not user: 
            errors = {
                "en": "Email does not match a user.",
                "da": "Email er ikke tilknyttet en bruger."
            }
            return g._SEND(400, errors[language])

        if not user_password == user['user_password']:
            errors = {
                "en": "Password is incorrect.",
                "da": "Kodeordet er ikke korrekt."
            }
            return g._SEND(400, errors[language]) 

        user_session = {
            "session_id": str(uuid.uuid4()),
            "user_id": user['user_id'],
            "iat": int(time.time())
        }

        session = db.execute("""INSERT INTO sessions
                                VALUES(
                                    :session_id,
                                    :user_id,
                                    :iat
                                )""", user_session)
        db.commit()

        encoded_jwt = jwt.encode(user_session, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt)

        return g._SEND(200, "Succesfull log in.") 

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()