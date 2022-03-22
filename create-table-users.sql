DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id                 TEXT UNIQUE NOT NULL,
    user_handle             TEXT UNIQUE NOT NULL,
    user_first_name         TEXT NOT NULL,
    user_last_name          TEXT NOT NULL,
    user_email              TEXT UNIQUE NOT NULL,
    user_password           TEXT NOT NULL,
    user_image_src          TEXT NOT NULL,
    user_description        TEXT NOT NULL,
    user_created_at         TEXT NOT NULL,
    user_created_at_date    TEXT NOT NULL,
    user_updated_at         TEXT NOT NULL,
    user_updated_at_date    TEXT NOT NULL,
    PRIMARY KEY(user_id)
) WITHOUT ROWID;