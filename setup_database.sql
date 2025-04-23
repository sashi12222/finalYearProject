CREATE DATABASE IF NOT EXISTS laundry;
USE laundry;

CREATE TABLE IF NOT EXISTS register (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    contact VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

CREATE TABLE IF NOT EXISTS laundry_service (
    laundry_id INT PRIMARY KEY,
    username VARCHAR(50),
    submit_date DATE,
    service_type VARCHAR(50),
    num_shirts VARCHAR(10),
    num_tshirts VARCHAR(10),
    num_shorts VARCHAR(10),
    num_pants VARCHAR(10),
    num_towels VARCHAR(10),
    num_suits VARCHAR(10),
    num_innerwears VARCHAR(10),
    num_kurtas VARCHAR(10),
    num_paijamas VARCHAR(10),
    num_skirts VARCHAR(10),
    image_file VARCHAR(255),
    stain_condition VARCHAR(50),
    delivery_date DATE,
    delivery_address TEXT,
    delivery_status VARCHAR(50),
    FOREIGN KEY (username) REFERENCES register(username)
); 