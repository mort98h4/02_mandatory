from bottle import get, request, view
import g
import jwt

##############################
@get("/explore")
@get("/<language>/explore")
# @view("explore")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"
        encoded_jwt = request.get_cookie("jwt")
        if encoded_jwt:
            decoded_jwt = jwt.decode(encoded_jwt, g.JWT_SECRET, algorithms=["HS256"])

            db = g._DB_CONNECT("database.sqlite")
            user = db.execute(""" SELECT sessions.session_id, users.user_id, users.user_handle, users.user_first_name, users.user_last_name, users.user_image_src, users.user_description, users.user_created_at
                                        FROM sessions
                                        JOIN users
                                        WHERE users.user_id = ? 
                                        AND sessions.session_id = ?""", (decoded_jwt['user_id'], decoded_jwt['session_id'])).fetchone()
            print("#"*30)
            print(decoded_jwt['session_id'])
            print(user)
            db.close()
            return user
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
        
    

    
