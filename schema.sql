CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL, 
    admin BOOLEAN
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY, 
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    name TEXT UNIQUE NOT NULL, 
    address TEXT NOT NULL, 
    city TEXT NOT NULL
);

CREATE TABLE r_stars (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    rating INTEGER
);

CREATE TABLE r_quetimes (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    que_time INTEGER
);

CREATE TABLE r_specialities (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    speciality TEXT
);

CREATE TABLE r_menus (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    food TEXT NOT NULL, 
    price NUMERIC NOT NULL
);

CREATE TABLE r_info (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    infotext TEXT, 
    open_times TEXT
);

CREATE TABLE likes_specialities (
    id SERIAL PRIMARY KEY, 
    liker_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    speciality_id INTEGER REFERENCES r_specialities(id) ON DELETE CASCADE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY, 
    r_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE, 
    u_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    message TEXT, 
    time TIMESTAMP
);
