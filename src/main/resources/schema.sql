-- Tạo database nếu chưa có
CREATE DATABASE IF NOT EXISTS coffee_shop_db;

-- Sử dụng database
USE coffee_shop_db;

-- Tạo bảng users nếu chưa có
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'STAFF') NOT NULL,
    enabled BOOLEAN DEFAULT TRUE
);

-- Tạo bảng menu_items nếu chưa có (tương thích với Coffee entity)
CREATE TABLE IF NOT EXISTS menu_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu users (mật khẩu đã được mã hóa BCrypt)
INSERT IGNORE INTO users (username, password, role, enabled) VALUES 
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVEFDa', 'ADMIN', TRUE),
('staff', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVEFDa', 'STAFF', TRUE);

-- Thêm dữ liệu mẫu menu
INSERT IGNORE INTO menu_items (name, description, price, category, available) VALUES 
('Espresso', 'Rich and bold espresso shot', 2.50, 'Coffee', TRUE),
('Cappuccino', 'Espresso with steamed milk and foam', 4.00, 'Coffee', TRUE),
('Latte', 'Espresso with steamed milk', 4.50, 'Coffee', TRUE),
('Americano', 'Espresso with hot water', 3.00, 'Coffee', TRUE),
('Mocha', 'Chocolate flavored coffee drink', 5.00, 'Coffee', TRUE);

-- Hiển thị kết quả
SELECT 'Users created:' as message;
SELECT * FROM users;
SELECT 'Menu items created:' as message;
SELECT * FROM menu_items;
