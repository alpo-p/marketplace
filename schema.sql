CREATE TABLE categories (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    name TEXT,
    date_added TIMESTAMP,
    visible BOOLEAN
);
CREATE TABLE iteminfo (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    price INTEGER,
    kuvaus TEXT,
    ostetaan BOOLEAN,
    picture TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
);
CREATE TABLE userinfo (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    puhelinnumero TEXT,
    paikkakunta TEXT,
    ptoimipaikka TEXT,
    sposti TEXT,
    osoite TEXT,
    kuvaus TEXT,
    nettisivu TEXT
);
CREATE TABLE admin(
    id SERIAL PRIMARY KEY,
    username TEXT
    password TEXT
)