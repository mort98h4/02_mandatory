from bottle import default_app, get, post, request, response, run, static_file, view
import uuid
import g

##############################
@get("/scripts/<script>")
def _(script):
    return static_file(script, root="./scripts")

##############################
@get("/")
@view("index")
def _():
    return

##############################
@post("/tweet")
@post("/<language>/tweet")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"

        # Validate
        tweet_text, error = g._IS_TWEET_TEXT(request.forms.get("tweet_text"), language)
        if error: return g._SEND(400, error)

        response.status = 201
        tweet_id = str(uuid.uuid4())
        tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
        }
        return tweet
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
   
    # Connect to the DB
    # Insert the tweet in the tweets table
    

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")