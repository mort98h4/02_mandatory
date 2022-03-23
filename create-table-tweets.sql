DROP TABLE IF EXISTS tweets;

CREATE TABLE tweets(
    tweet_id                TEXT UNIQUE NOT NULL,
    tweet_text              TEXT NOT NULL,
    tweet_image_src         TEXT NOT NULL,
    tweet_created_at        TEXT NOT NULL,
    tweet_created_at_date   TEXT NOT NULL,
    tweet_updated_at        TEXT NOT NULL,
    tweet_updated_at_date   TEXT NOT NULL,
    user_id                 TEXT NOT NULL,
    PRIMARY KEY(tweet_id)    
) WITHOUT ROWID;