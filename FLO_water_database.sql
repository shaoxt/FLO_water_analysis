CREATE DATABASE FLO_water;
USE FLO_water;

CREATE TABLE water_usage (id INT AUTO_INCREMENT primary key NOT NULL, timestamp timestamp, psi decimal(15,5), gpm decimal(15,5));
ALTER TABLE water_usage ALTER psi SET DEFAULT 0;
ALTER TABLE water_usage ALTER gpm SET DEFAULT 0;

CREATE TABLE sensor_data (
   id INT AUTO_INCREMENT primary key NOT NULL,
   sensor VARCHAR(50),
   date_created timestamp default NOW(),
   value decimal(15,5),
   UNIQUE INDEX(date_created, sensor)
);