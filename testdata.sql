DELETE FROM messages;
DELETE FROM r_menus;
DELETE FROM r_info;
DELETE FROM r_stars;
DELETE FROM r_quetimes;
DELETE FROM restaurants;
DELETE FROM users;





INSERT INTO users (id, username, password, admin) VALUES (901, 'Sodexo','12345',True);
INSERT INTO users (id, username, password, admin) VALUES (902, 'Unicafe','12345',True);


INSERT INTO users (id, username, password, admin) VALUES (903, 'Kalevi','12345',False);
INSERT INTO users (id, username, password, admin) VALUES (904, 'Sanni','12345',False);

INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (1, 901 ,'Päärakennus','Aleksanterinkatu 32','Helsinki');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (2, 902 ,'Kaivopiha','Lönrotinkatu 32','Helsinki');

INSERT INTO messages (r_id, u_id, message, time) VALUES (1, 903, 'Hyvää ruokaa tänään', NOW());
INSERT INTO messages (r_id, u_id, message, time) VALUES (2, 904, 'Huonoa ruokaa tänään...', NOW());

INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Hernekeitto', 2.85);

INSERT INTO r_info (r_id, infotext, open_times) VALUES (1, 'Tulkaa etuovesta', '11-15');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (2, 'Tulkaa takaovesta', '11.30-14');

INSERT INTO r_stars (r_id, rating) VALUES (1, 5);
INSERT INTO r_stars (r_id, rating) VALUES (1, 4);

INSERT INTO r_stars (r_id, rating) VALUES (2, 3);
INSERT INTO r_stars (r_id, rating) VALUES (2, 2);
INSERT INTO r_stars (r_id, rating) VALUES (2, 3);

INSERT INTO r_quetimes (r_id, que_time) VALUES (1, 10);
INSERT INTO r_quetimes (r_id, que_time) VALUES (1, 11);

INSERT INTO r_quetimes (r_id, que_time) VALUES (2, 7);
INSERT INTO r_quetimes (r_id, que_time) VALUES (2, 9);






