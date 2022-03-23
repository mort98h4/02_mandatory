from bottle import delete, response
import g
import os

##############################
@delete("/tweet/<id>")
@delete("/<language>/tweet/<id>")
def _(language="en", id=""):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"

        tweet_id, error = g._IS_UUID4(id, language)
        if error: return g._SEND(400, error)

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db = g._DB_CONNECT("database.sqlite")
        
        tweet_image_src = db.execute("""SELECT tweets.tweet_image_src 
                                        FROM tweets
                                        WHERE tweet_id = ?""", (tweet_id,)).fetchone()
        counter = db.execute("DELETE FROM tweets WHERE tweet_id = ?", (tweet_id,)).rowcount
        db.commit()
        if not counter: return g._SEND(204, "")
        if tweet_image_src['tweet_image_src'] != "": os.remove(f"./images/{tweet_image_src['tweet_image_src']}")
        response.status = 200
        return {"info": "Tweet deleted."}
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    finally: 
        db.close()

