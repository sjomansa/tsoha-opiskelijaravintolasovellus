DELETE FROM messages;
DELETE FROM r_menus;
DELETE FROM r_info;
DELETE FROM r_stars;
DELETE FROM r_quetimes;
DELETE FROM restaurants;
DELETE FROM users;





INSERT INTO users (id, username, password, admin) VALUES (901, 'Sodexo','12345',True);
INSERT INTO users (id, username, password, admin) VALUES (902, 'Unicafe','12345',True);
INSERT INTO users (id, username, password, admin) VALUES (905, 'Fazer','12345',True);
INSERT INTO users (id, username, password, admin) VALUES (906, 'Compass-Group','12345',True);


INSERT INTO users (id, username, password, admin) VALUES (903, 'Kalevi','12345',False);
INSERT INTO users (id, username, password, admin) VALUES (904, 'Sanni','12345',False);

INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (1, 901 ,'Päärakennus','Aleksanterinkatu 32','Helsinki');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (2, 902 ,'Kaivopiha','Lönrotinkatu 32','Helsinki');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (3, 901 ,'Tekniikkatalo','Tekniikkatie 15','Espoo');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (4, 901 ,'Sivurakennus','Santerinterinkatu 10','Helsinki');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (5, 905 ,'Musiikkitalo','Mannerheiminkatu 56','Helsinki');
INSERT INTO restaurants (id, owner_id, name, address, city) VALUES (6, 906 ,'Metsätalo','Helsingintie 3','Helsinki');



INSERT INTO messages (r_id, u_id, message, time) VALUES (1, 903, 'Hyvää ruokaa tänään', NOW());
INSERT INTO messages (r_id, u_id, message, time) VALUES (2, 904, 'Huonoa ruokaa tänään...', NOW());

INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (1, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (2, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (3, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (3, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (3, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (4, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (4, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (4, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (5, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (5, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (5, 'Hernekeitto', 2.85);

INSERT INTO r_menus (r_id, food, price) VALUES (6, 'Makaronilaatikko', 2.95);
INSERT INTO r_menus (r_id, food, price) VALUES (6, 'Soijarouhekebab', 2.85);
INSERT INTO r_menus (r_id, food, price) VALUES (6, 'Hernekeitto', 2.85);

INSERT INTO r_info (r_id, infotext, open_times) VALUES (1, 'Tulkaa etuovesta', '11-15');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (2, 'Tulkaa takaovesta', '11.30-14');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (3, 'Tulkaa takaovesta', '11.30-14');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (4, 'Tulkaa takaovesta', '11.30-14');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (5, 'Tulkaa takaovesta', '11.30-14');
INSERT INTO r_info (r_id, infotext, open_times) VALUES (6, 'Tulkaa takaovesta', '11.30-14');

INSERT INTO r_stars (r_id, rating) VALUES (1, 5);
INSERT INTO r_stars (r_id, rating) VALUES (1, 4);

INSERT INTO r_stars (r_id, rating) VALUES (2, 3);
INSERT INTO r_stars (r_id, rating) VALUES (2, 2);
INSERT INTO r_stars (r_id, rating) VALUES (2, 3);

INSERT INTO r_stars (r_id, rating) VALUES (3, 3);
INSERT INTO r_stars (r_id, rating) VALUES (3, 5);
INSERT INTO r_stars (r_id, rating) VALUES (3, 3);

INSERT INTO r_stars (r_id, rating) VALUES (4, 1);
INSERT INTO r_stars (r_id, rating) VALUES (4, 1);
INSERT INTO r_stars (r_id, rating) VALUES (4, 2);

INSERT INTO r_stars (r_id, rating) VALUES (5, 3);
INSERT INTO r_stars (r_id, rating) VALUES (5, 1);
INSERT INTO r_stars (r_id, rating) VALUES (5, 1);

INSERT INTO r_stars (r_id, rating) VALUES (6, 5);
INSERT INTO r_stars (r_id, rating) VALUES (6, 5);
INSERT INTO r_stars (r_id, rating) VALUES (6, 4);

INSERT INTO r_quetimes (r_id, que_time) VALUES (1, 10);
INSERT INTO r_quetimes (r_id, que_time) VALUES (1, 11);

INSERT INTO r_quetimes (r_id, que_time) VALUES (2, 7);
INSERT INTO r_quetimes (r_id, que_time) VALUES (2, 9);

INSERT INTO r_quetimes (r_id, que_time) VALUES (3, 7);
INSERT INTO r_quetimes (r_id, que_time) VALUES (4, 9);

INSERT INTO r_quetimes (r_id, que_time) VALUES (5, 25);
INSERT INTO r_quetimes (r_id, que_time) VALUES (5, 9);
INSERT INTO r_quetimes (r_id, que_time) VALUES (5, 19);
INSERT INTO r_quetimes (r_id, que_time) VALUES (5, 20);

INSERT INTO r_quetimes (r_id, que_time) VALUES (6, 40);
INSERT INTO r_quetimes (r_id, que_time) VALUES (6, 39);
INSERT INTO r_quetimes (r_id, que_time) VALUES (6, 38);
INSERT INTO r_quetimes (r_id, que_time) VALUES (6, 37);






