from bottle import post, response, request
import uuid
import g
import time
from datetime import datetime

##############################
@post("/tweet")
@post("/<language>/tweet")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"

        # Validate
        tweet_text, error = g._IS_TWEET_TEXT(request.forms.get("tweet_text"), language)
        if error: return g._SEND(400, error)

        tweet_id = str(uuid.uuid4())

        tweet_image_src = ""
        if request.files.get("tweet_image_src"):
            tweet_image_src, error = g._IS_TWEET_IMAGE(request.files.get("tweet_image_src"), language)
            if error: return g._SEND(400, error) 

        tweet_created_at = str(int(time.time()))
        tweet_created_at_date = datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        tweet_updated_at = ""
        tweet_updated_at_date = ""
        user_id = request.forms.get("user_id")
        
        tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
            "tweet_image_src" : tweet_image_src,
            "tweet_created_at" : tweet_created_at,
            "tweet_created_at_date" : tweet_created_at_date,
            "tweet_updated_at" : tweet_updated_at,
            "tweet_updated_at_date" : tweet_updated_at_date,
            "user_id": user_id
        }
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    
    try:
        db = g._DB_CONNECT("database.sqlite")
        db.execute("""INSERT INTO tweets
                      values(
                          :tweet_id,
                          :tweet_text,
                          :tweet_image_src,
                          :tweet_created_at,
                          :tweet_created_at_date,
                          :tweet_updated_at,
                          :tweet_updated_at_date,
                          :user_id
                      )""", tweet)
        db.commit()

        tweet = db.execute("""SELECT tweets.tweet_id, tweets.tweet_text, tweets.tweet_image_src, tweets.tweet_created_at, tweets.tweet_created_at_date, tweets.tweet_updated_at, tweets.tweet_updated_at_date, tweets.user_id, users.user_handle, users.user_first_name, users.user_last_name, users.user_image_src
                              FROM tweets
                              JOIN users
                              WHERE tweets.tweet_id = ?
                              AND users.user_id = ?
                              """, (tweet['tweet_id'], tweet['user_id'],)).fetchone()

        response.status = 201
        return tweet
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()
    # Connect to the DB
    # Insert the tweet in the tweets table