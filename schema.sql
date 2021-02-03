CREATE TABLE categories (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    name TEXT);