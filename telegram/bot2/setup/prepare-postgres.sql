create database sp;
create user bot with encrypted password 'bopass';

GRANT ALL ON ALL TABLES IN SCHEMA "public" TO bot;
GRANT ALL PRIVILEGES ON DATABASE sp TO bot;

GRANT ALL ON DATABASE sp TO bot;
GRANT ALL ON SCHEMA public to bot;
GRANT ALL ON ALL TABLES IN SCHEMA public TO bot;


\c sp;

CREATE TABLE IF NOT EXISTS watcher (
    user_id         VARCHAR ( 50 ) NOT NULL,
    yf_id           VARCHAR ( 50 ) NOT NULL, 
    minValue        NUMERIC( 10, 3),
    maxValue        NUMERIC( 10, 3),
    var_last        TIMESTAMP,
    minValue_last   TIMESTAMP,
    maxVaule_last   TIMESTAMP,
    UNIQUE (user_id, yf_id)
);

CREATE TABLE IF NOT EXISTS symbol (
    yf_id           VARCHAR ( 50 ) UNIQUE NOT NULL,
    displayName     VARCHAR ( 80 ),
    marketState     VARCHAR ( 50 ),
    previousClose   NUMERIC( 10, 3),
    lastPrice       NUMERIC( 10, 3),
    currency        VARCHAR ( 50 ),
    _var            NUMERIC( 5, 2),
    _lastCheck      TIMESTAMP      
);



        