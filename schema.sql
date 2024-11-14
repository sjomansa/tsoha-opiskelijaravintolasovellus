CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, owner_id INTEGER REFERENCES users, name TEXT UNIQUE, address TEXT, city TEXT);
CREATE TABLE r_stars (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, rating INTEGER);
CREATE TABLE r_quetimes (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, que_time INTEGER);
CREATE TABLE r_specialities (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, speciality TEXT);
CREATE TABLE r_menus (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, food TEXT, price NUMERIC);
CREATE TABLE r_info (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, infotext TEXT, open_times TEXT);
CREATE TABLE likes_specialities (id SERIAL PRIMARY KEY, liker_id INTEGER REFERENCES users, speciality_id INTEGER REFERENCES r_specialities);
CREATE TABLE messages (id SERIAL PRIMARY KEY, r_id INTEGER REFERENCES restaurants, u_id INTEGER REFERENCES users, message TEXT, time TIMESTAMP);
