CREATE TABLE categories (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    name TEXT,
    date_added TIMESTAMP,
    visible BOOLEAN,
    user_id INTEGER REFERENCES users,
    price INTEGER,
    kuvaus TEXT,
    picture TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE userinfo (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    puhelinnumero TEXT,
    paikkakunta TEXT,
    sposti TEXT,
    kuvaus TEXT,
);

CREATE TABLE admin(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);