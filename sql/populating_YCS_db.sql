USE `YCS`;

create table city_index(
    city_id INT NOT NULL auto_increment,
    city_name VARCHAR(32) NOT NULL,
    walkability double,
    transit double,
    pop_density double,
    bikeability double,
    crime double,
    PRIMARY KEY (city_id)
);

ALTER TABLE city_index
ADD population double;

ALTER TABLE city_index
DROP crime;

ALTER TABLE city_index
CHANGE COLUMN population metro_population double;

ALTER TABLE city_index
CHANGE COLUMN air_quality air_pollution double;

INSERT INTO city_index
    (city_name, population, transit, walkability, bikeability)
VALUES
("New York", 20320876, 84.3, 89.2, 67.7),
("Los Angeles", 13353907, 52.6, 67.4, 55.1),
("Chicago", 9533040, 65.3, 77.8, 71.5),
("Dallas", 7399662, 39.7, 46.2, 46.4),
("Houston", 6892427, 36.9, 48.7, 47.9),
("Washington DC", 6216589, 70.7, 77.3, 66.9),
("Miami", 6158824, 56.8, 79.2, 63.0),
("Philadelphia", 6096120, 66.8, 79.0, 65.6),
("Atlanta", 5884736, 47.2, 49.2, 41.4),
("Boston", 4836531, 72.5, 80.9, 69.0),
("Phoenix", 4737270, 36.0, 40.8, 52.4),
("San Francisco", 4727357, 80.3, 86.0, 70.7),
("Riverside", 4580670, 32.6, 41.3, 44.7),
("Detroit", 4313002, 38.8, 55.4, 51.5),
("Seattle", 3867046, 60.1, 73.1, 70.0),
("Minneapolis", 3600618, 57.0, 69.2, 81.9),
("San Diego", 3337685, 36.9, 50.9, 39.4),
("Tampa", 3091399, 33.5, 50.0, 54.5),
("Denver", 2888227, 47.5, 60.5, 71.3),
("Baltimore", 2808175, 56.9, 69.4, 52.1),
("St. Louis", 2807338, 45.3, 64.5, 53.0),
("Charlotte", 2525305, 28.7, 25.9, 30.4),
("Orlando", 2509831, 32.6, 42.1, 54.8),
("San Antonio", 2473974, 35.7, 37.6, 41.9),
("Portland", 2453168, 51.6, 64.7, 81.2);

create table users(
    user_id INT NOT NULL auto_increment,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id)
);

INSERT INTO city_index
    (city_id, prop_crime, violent_crime, air_quality, pop_density)
VALUES
(1, 1448.59, 538.90, 57.08, 28317),
(2, 2535.92, 761.31, 60.35, 8484),
(3, 3263.80, 1098.86, 41.03, 11900),
(4, 3185.09, 774.64, 39.80, 3866),
(5, 4128.41, 1095.23, 52.36, 3613),
(6, 4156.22, 948.74, 39.26, 11148),
(7, 4014.18, 720.94, 37.91, 12599),
(8, 3063.48, 947.58, 51.82, 11683),
(9, 4776.43, 935.74, 44.70, 3539),
(10, 2089.02, 669.20, 25.29, 13938),
(11, 3670.71, 760.93, 61.42, 3120),
(12, 6168.02, 715.00, 35.15, 18569),
(13, 3058.32, 508.81, 46.48, 3999),
(14, 4540.60, 2056.67, 55.17, 4847),
(15, 5258.64, 675.61, 27.96, 8405),
(16, 4641.37, 1101.27, 23.49, 7660),
(17, 1842.97, 366.61, 34.82, 4325),
(18, 1743.68, 464.41, 28.93, 3326),
(19, 3667.06, 675.61, 41.23, 4521),
(20, 4928.11, 2027.01, 45.14, 7598),
(21, 6041.24, 2028.29, 35.19, 5023),
(22, 3815.18, 338.00, 28.22, 2757),
(23, 5454.57, 744.06, 34.29, 2635),
(24, 4844.84, 707.50, 39.40, 3238),
(25, 5677.02, 515.70, 27.19, 4793)
ON DUPLICATE KEY UPDATE prop_crime = VALUES(prop_crime),
violent_crime = VALUES(violent_crime), air_quality = VALUES(air_quality),
pop_density = VALUES(pop_density);

select *
from city_index;