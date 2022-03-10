from bottle import get, run

##############################
@get("/")
def _():
    return "hi"
    
##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")