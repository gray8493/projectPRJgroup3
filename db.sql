-- Tạo database cho hệ thống POS cafe
CREATE DATABASE IF NOT EXISTS cafe_pos;
USE cafe_pos;

-- Tạo bảng users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tạo bảng menu_items
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu users
INSERT INTO users (username, password, name, role) VALUES
('admin', '$2b$10$rQZ8K9LmN2pO3qR4sT5uVe6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oP6', 'Quản trị viên', 'admin'),
('staff', '$2b$10$rQZ8K9LmN2pO3qR4sT5uVe6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oP6', 'Nhân viên', 'staff');

-- Tạo bảng orders để lưu đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_type ENUM('dine-in', 'takeaway', 'delivery') NOT NULL,
    table_number INT NULL,
    staff_username VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tạo bảng order_items để lưu chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Thêm dữ liệu mẫu menu_items
INSERT INTO menu_items (name, price, category) VALUES
('Cà phê đen', 15000, 'coffee'),
('Cà phê sữa', 18000, 'coffee'),
('Cappuccino', 25000, 'coffee'),
('Latte', 28000, 'coffee'),
('Trà đào', 20000, 'tea'),
('Trà sữa', 22000, 'tea'),
('Trà chanh', 18000, 'tea'),
('Nước cam', 15000, 'juice'),
('Nước táo', 15000, 'juice'),
('Sinh tố dâu', 25000, 'smoothie'),
('Sinh tố xoài', 25000, 'smoothie'),
('Bánh mì pate', 15000, 'snack'),
('Bánh ngọt', 12000, 'snack');
