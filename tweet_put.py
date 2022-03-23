from bottle import put, request
import g
import time
from datetime import datetime
import os
import json

##############################
@put("/tweet/<id>")
@put("/<language>/tweet/<id>")
def _(language = "en", id=""):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"

        tweet_id, error = g._IS_UUID4(id, language)
        if error: return g._SEND(400, error)
        
        allowed_keys = ["tweet_id", "tweet_text", "tweet_image_src"]
        for key in request.forms.keys():
            if not key in allowed_keys:
                print(key)
                return g._SEND(400, f"Forbidden {key}.")

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db = g._DB_CONNECT("database.sqlite")
        tweet = db.execute("SELECT * FROM tweets WHERE tweet_id = ?", (tweet_id,)).fetchone()
        image_path = (tweet['tweet_image_src'])
        if not tweet: return g._SEND(204, "")

        for key in tweet.keys():
            if key in request.forms.keys():
                tweet[key] = request.forms.get(key)
        
        tweet_text, error = g._IS_TWEET_TEXT(tweet['tweet_text'], language)
        if error: return g._SEND(400, error)
        if request.files.get("tweet_image_src"):
            tweet_image_src, error = g._IS_TWEET_IMAGE(request.files.get("tweet_image_src"), language)
            if error: return g._SEND(400, error)
        else:
            tweet_image_src = ""

        tweet['tweet_text'] = tweet_text
        tweet['tweet_image_src'] = tweet_image_src
        tweet['tweet_updated_at'] = str(int(time.time()))
        now = datetime.now()
        tweet['tweet_updated_at_date'] = now.strftime("%Y-%B-%d-%A %H:%M:%S")
        
        counter = db.execute("""UPDATE tweets
                                SET tweet_text=:tweet_text,
                                tweet_image_src=:tweet_image_src,
                                tweet_updated_at=:tweet_updated_at,
                                tweet_updated_at_date=:tweet_updated_at_date
                                WHERE tweet_id = :tweet_id""", tweet).rowcount
        db.commit()
        if not counter: return g._SEND(204, "")
        if image_path != "": os.remove(f"./images/{image_path}")
        return json.dumps(tweet)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()