-- Tạo database cho hệ thống POS cafe
CREATE DATABASE IF NOT EXISTS cafe_pos;
USE cafe_pos;

-- Tạo bảng menu_items
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu
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
