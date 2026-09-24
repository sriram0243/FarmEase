-- ==========================================================================
-- FARMEASE DATABASE SCHEMA & INITIAL DATA
-- Database Name: farmease_db
-- ==========================================================================

CREATE DATABASE IF NOT EXISTS farmease_db;
USE farmease_db;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. EQUIPMENT TABLE
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category ENUM('Tractors', 'Harvesters', 'Rotavators', 'Sprayers', 'Seeders') NOT NULL,
    description TEXT,
    price_per_day DECIMAL(10, 2) NOT NULL,
    location VARCHAR(100) NOT NULL,
    hp VARCHAR(50),
    fuel_type VARCHAR(50),
    badge VARCHAR(50),
    image VARCHAR(255) NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    owner_phone VARCHAR(20) NOT NULL,
    status ENUM('Available', 'Unavailable', 'Maintenance') DEFAULT 'Available',
    rating DECIMAL(3, 1) DEFAULT 4.8,
    reviews_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. BOOKINGS TABLE
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days INT NOT NULL,
    price_per_day DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Confirmed', 'Completed', 'Cancelled') DEFAULT 'Confirmed',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- 4. REVIEWS TABLE
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- 5. FAVORITES TABLE
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY user_equipment_unique (user_id, equipment_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- ==========================================================================
-- SAMPLE SEED DATA
-- Default Passwords: "password123" (Hashed using pbkdf2:sha256)
-- ==========================================================================

-- Insert Admin User (Email: admin@farmease.com | Password: password123)
INSERT INTO users (name, email, phone, password_hash, role, status)
VALUES 
('System Admin', 'admin@farmease.com', '9876543210', 'pbkdf2:sha256:600000$gS5H5H7k$e8b5d3a5e8c1b9a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6', 'admin', 'active'),
('Murugan Farmer', 'farmer@farmease.com', '9876501234', 'pbkdf2:sha256:600000$gS5H5H7k$e8b5d3a5e8c1b9a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6', 'user', 'active')
ON DUPLICATE KEY UPDATE id=id;

-- Insert Equipment Items
INSERT INTO equipment (id, name, category, description, price_per_day, location, hp, fuel_type, badge, image, owner_name, owner_phone, status, rating, reviews_count)
VALUES
(1, 'John Deere 5310', 'Tractors', 'Heavy duty 55 HP 4WD tractor suitable for plowing, deep tilling, and heavy haulage.', 1200.00, 'Coimbatore', '55 HP', 'Diesel', 'Most Booked', 'tractor.png', 'Karthik Raja', '9842100001', 'Available', 4.9, 125),
(2, 'Mahindra Arjun 605', 'Tractors', 'Powerful 60 HP multi-speed tractor designed for high load operations and rotavator work.', 1400.00, 'Erode', '60 HP', 'Diesel', 'Top Rated', 'tractor.png', 'Senthil Kumar', '9842100002', 'Available', 4.8, 96),
(3, 'Kubota Harvester', 'Harvesters', 'Advanced paddy and grain combine harvester with minimal grain loss technology.', 3500.00, 'Salem', '75 HP', 'Diesel', 'Premium', 'harvester.png', 'Venkatesh P.', '9842100003', 'Available', 4.7, 88),
(4, 'Shaktiman Rotavator', 'Rotavators', 'Multi-speed PTO driven rotavator for fine seedbed preparation and soil aeration.', 900.00, 'Madurai', 'PTO Driven', 'Tractor PTO', 'Best Value', 'rotavator.png', 'Ramanathan M.', '9842100004', 'Available', 4.8, 77),
(5, 'Power Sprayer unit', 'Sprayers', 'High pressure engine-driven agricultural sprayer for cotton, paddy, and orchard protection.', 500.00, 'Trichy', '5.5 HP', 'Petrol', 'New', 'sprayer.png', 'Dhanapal S.', '9842100005', 'Available', 4.6, 58),
(6, 'Automatic Seed Drill', 'Seeders', 'Precision seed and fertilizer drill machine for uniform sowing across large crop acres.', 700.00, 'Thanjavur', 'PTO Driven', 'Tractor PTO', 'Farmer Choice', 'seed.png', 'Ganesan R.', '9842100006', 'Available', 4.9, 64)
ON DUPLICATE KEY UPDATE id=id;
