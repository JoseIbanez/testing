create database sp;
create user bot with encrypted password 'bopass';

grant all privileges on database sp to bot;
GRANT ALL ON ALL TABLES IN SCHEMA "public" TO bot;



\c sp;

CREATE TABLE [IF NOT EXISTS] watcher (
   column1 datatype(length) column_contraint,
   column2 datatype(length) column_contraint,
   column3 datatype(length) column_contraint,
   table_constraints
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



        