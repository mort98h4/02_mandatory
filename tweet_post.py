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
            tweet_image_src, error = g._IS_TWEET_IMAGE(request.files.get("tweet_image_src"), tweet_id, language)
            if error: return g._SEND(400, error) 

        tweet_created_at = str(int(time.time()))
        tweet_created_at_date = datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        tweet_updated_at = ""
        tweet_updated_at_date = ""

        # TODO: Get the user_id as well
        
        tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
            "tweet_image_src" : tweet_image_src,
            "tweet_created_at" : tweet_created_at,
            "tweet_created_at_date" : tweet_created_at_date,
            "tweet_updated_at" : tweet_updated_at,
            "tweet_updated_at_date" : tweet_updated_at_date
        }
        response.status = 201
        return tweet
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
   
    # Connect to the DB
    # Insert the tweet in the tweets table