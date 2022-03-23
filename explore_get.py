from bottle import get, request, view
import g
import jwt

##############################
@get("/explore")
@get("/<language>/explore")
@view("explore")
def _(language = "en"):
    user = {}
    tweets = []

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
            db.close()
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    
    try: 
        db = g._DB_CONNECT("database.sqlite")
        tweets = db.execute("""SELECT tweets.tweet_id, tweets.tweet_text, tweets.tweet_image_src, tweets.tweet_created_at, tweets.tweet_created_at_date, tweets.tweet_updated_at, tweets.tweet_updated_at_date, tweets.user_id, users.user_handle, users.user_first_name, users.user_last_name, users.user_image_src
                               FROM tweets
                               JOIN users
                               WHERE tweets.user_id = users.user_id
                               ORDER BY tweet_created_at DESC""").fetchall()
        
        return dict(user=user, tweets=tweets)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally: 
        db.close()