from bottle import response
import re
import os
import imghdr
import time
from datetime import datetime

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

ERRORS = {
    "en_server_error": "Server error",
    "da_server_error": "Server fejl"
}

JWT_SECRET = "4w50m3 k3Y"

##############################
users = [
    {"user_id":"af1cf565-1c2d-4673-948d-6544276b54b2", "user_handle":"mortengross", "user_first_name":"Morten", "user_last_name":"Gross", "user_email":"m@g.dk", "user_password":"123456Qw", "user_image_src":"03e2f8bd-3453-47d7-907b-9cc9c1adcc28.png", "user_description":"Some description", "user_created_at":str(int(time.time())), "user_created_at_date":datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"), "user_updated_at":"", "user_updated_at_date":""}
]

sessions = []

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

##############################
def _IS_TWEET_IMAGE(image=None, id=None, language="en"):
    errors_file_not_allowed = {
        "en": "Filetype is not allowed",
        "da": "Filtypen er ikke tilladt."
    }
    errors_suspicious_file = {
        "en": "Suspicious image file.",
        "da": "Mistænkelig billedfil."
    }

    file_name, file_extension = os.path.splitext(image.filename)
    if file_extension not in (".png", ".jpeg", ".jpg"): return None, errors_file_not_allowed[language]
    if file_extension == ".jpg": file_extension = ".jpeg"
    image_name = f"{id}{file_extension}"
    image.save(f"./images/{image_name}")
    imghdr_extension = imghdr.what(f"./images/{image_name}")
    if not file_extension == f".{imghdr_extension}":
        os.remove(f"./images/{image_name}")
        return None, errors_suspicious_file[language]
    return image_name, None

##############################
def _IS_NAME(name=None, language="en", name_type="first"):
    name_type = name_type.capitalize()
    min, max = 2, 30
    errors_name_missing = {
        "en": f"{name_type} name is missing.",
        "da": "Navn mangler."
    }
    errors_min = {
        "en": f"{name_type} first name must be at least {min}",
        "da": f"Navn skal minimum indholde {min} tegn."
    }
    errors_max = {
        "en": f"{name_type} name is not allowed to exceed {max} characters.",
        "da": f"Navn må ikke være mere end {max} tegn."
    }

    if not name: return None, errors_name_missing[language]
    name = re.sub("[\n\t]*", "", name)
    name = re.sub(" +", " ", name)
    name = name.strip()
    if len(name) < min: return None, errors_min[language]
    if len(name) > max: return None, errors_max[language]
    name = name.capitalize()
    return name, None

##############################
def _IS_EMAIL(email=None, language="en"):
    errors_missing = {
        "en":"Email is missing.",
        "da":"Email mangler."
    }
    errors_invalid = {
        "en":"Email is invalid",
        "da":"Ugyldig email."
    }

    if not email: return None, errors_missing[language]
    email = email.strip()
    if not re.match(REGEX_EMAIL, email): return None, errors_invalid[language]
    return email, None

##############################
def _IS_HANDLE(handle=None, language="en"):
    min, max = 2, 30
    errors_missing = {
        "en":"Username is missing",
        "da":"Brugernavn mangler."
    }
    errors_min = {
        "en":f"Username must be at least {min} characters.",
        "da":f"Brugernavn skal minimum være {min} tegn."
    }
    errors_max = {
        "en":f"Username is not allowed to exceed {max} characters.",
        "da":f"Brugernavn må ikke være mere end {max} tegn."
    }
    errors_invalid_characters = {
        "en":"Username can only contain alphanumeric characters, '.' or '_'.",
        "da":"Brugernavn må kun indeholde tal, bogstaver, '.' eller '_'."
    }
    errors_invalid_character_succesion = {
        "en":"Username must not begin or end with '.' or '_' and they must not succeed each other either.",
        "da":"Brugernavn må ikke begynde eller ende med '.' eller '_', og de må ikke efterfølge hinanden."

    }
    if not handle: return None, errors_missing[language]
    if len(handle) < min: return None, errors_min[language]
    if len(handle) > max: return None, errors_max[language]
    if not re.match("^[a-zA-Z0-9\\._]*$", handle): return None, errors_invalid_characters[language]
    if not re.match("^(?!.*[_.]{2})[^_.].*[^_.]$", handle): return None, errors_invalid_character_succesion[language]
    return handle, None

##############################
def _ALREADY_EXISTS(value=None, field="", language="en"):
    errors = {
        "en":f"{field} already exists in users.",
        "da":f"{field} findes allerede i users."
    }
    for user in users:
        if value.lower() == user[field].lower():
            return None, errors[language]
    return value, None

##############################
def _IS_PASSWORD(password=None, language="en"):
    errors_missing = {
        "en":"Password is missing.",
        "da":"Kodeord mangler."
    }
    errors_invalid = {
        "en":"Password must be at least 8 characters containing at least 1 uppercase letter, 1 lowercase letter and 1 number.",
        "da":"Kodeord skal minimum være 8 tegn langt, og indeholde minimum 1 stort bogstav, 1 lille bogstav og 1 tal."
    }
    if not password: return None, errors_missing[language]
    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password): return None, errors_invalid[language]
    return password, None