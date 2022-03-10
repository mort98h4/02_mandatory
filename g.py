from bottle import response
import re

ERRORS = {
    "en_server_error": "Server error",
    "da_server_error": "Server fejl"
}

##############################
def _SEND(status = 400, error_message = "Unknown error"):
    response.status = status
    return {"info": error_message}

##############################
def _IS_TWEET_TEXT(text=None, language="en"):
    min, max = 1, 255
    errors_text_missing = {
        "en": "Tweet_text is missing.",
        "da": "Tweet_text mangler."
    }
    errors_min = {
        "en": f"Tweet_text must be at least {min} character.",
        "da": f"Tweet_text skal minimum indeholde {min} tegn."
    }
    errors_max = {
        "en": f"Tweet_text must be less than {max} characters.",
        "da": f"Tweet_text må maksimum indeholde {max} tegn."
    }

    if not text: return None, errors_text_missing[language]
    text = re.sub("[\n\t]*", "", text)
    text = re.sub(" +", " ", text)
    text = text.strip()
    if len(text) < min: return None, errors_min[language]
    if len(text) > max: return None, errors_max[language]
    text = text.capitalize()
    return text, None