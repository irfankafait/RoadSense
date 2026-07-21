CREATE TABLE IF NOT EXISTS locations (

    location_id INT AUTO_INCREMENT PRIMARY KEY,

    location_name VARCHAR(100) NOT NULL UNIQUE
    );

CREATE TABLE IF NOT EXISTS weather (

    weather_id INT AUTO_INCREMENT PRIMARY KEY,

    weather_name VARCHAR(100) NOT NULL UNIQUE

);

CREATE TABLE IF NOT EXISTS severity (

    severity_id INT AUTO_INCREMENT PRIMARY KEY,

    severity_name VARCHAR(100) NOT NULL UNIQUE

);

CREATE TABLE IF NOT EXISTS road_types (

    road_type_id INT AUTO_INCREMENT PRIMARY KEY,

    road_type_name VARCHAR(100) NOT NULL UNIQUE

);

CREATE TABLE IF NOT EXISTS zones (

    zone_id INT AUTO_INCREMENT PRIMARY KEY,

    zone_name VARCHAR(100) NOT NULL UNIQUE

);




CREATE TABLE IF NOT EXISTS accidents (

    accident_id INT AUTO_INCREMENT PRIMARY KEY,

    accident_date DATE NOT NULL,

    hour_of_day INT NOT NULL,

    location_id INT NOT NULL,

    zone_id INT NOT NULL,

    weather_id INT NOT NULL,

    severity_id INT NOT NULL,

    road_type_id INT NOT NULL,

    latitude DECIMAL (10,6),

    longitude DECIMAL (10, 6),


    FOREIGN KEY (location_id)
        REFERENCES locations(location_id),

    FOREIGN KEY (weather_id)
        REFERENCES weather(weather_id),

    FOREIGN KEY (severity_id)
        REFERENCES severity(severity_id),

    FOREIGN KEY (road_type_id)
        REFERENCES road_types(road_type_id),

    FOREIGN KEY (zone_id)
        REFERENCES zones(zone_id)    

);           