DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions(
    session_id              TEXT UNIQUE NOT NULL,
    user_id                 TEXT NOT NULL,
    iat                     TEXT NOT NULL,
    PRIMARY KEY(session_id)
) WITHOUT ROWID;