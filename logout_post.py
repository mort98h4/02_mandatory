from bottle import post, redirect, request, response
import g
import jwt

##############################
@post("/logout")
@post("/<language>/logout")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"
    try:
        encoded_jwt = request.get_cookie("jwt")
        session = jwt.decode(encoded_jwt, g.JWT_SECRET, algorithms=["HS256"])

        session_id, error = g._IS_UUID4(session['session_id'], language)
        if error: return g._SEND(400, error)

        # return session_id
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db = g._DB_CONNECT("database.sqlite")
        counter = db.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,)).rowcount
        db.commit()
        if not counter: return g._SEND(204, "")
        response.set_cookie("jwt", encoded_jwt, expires=0)
        return g._SEND(200, "Session deleted.")

    except Exception as ex: 
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()
        return redirect("/")