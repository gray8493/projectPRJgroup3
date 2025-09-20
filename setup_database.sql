-- Script thiết lập database cho hệ thống quét khuôn mặt
-- Chạy script này trong MySQL để tạo database và bảng

-- Tạo database
CREATE DATABASE IF NOT EXISTS face_recognition 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Sử dụng database
USE face_recognition;

-- Tạo bảng face_scans (thông tin các lần quét)
CREATE TABLE IF NOT EXISTS face_scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scan_time DATETIME NOT NULL,
    face_count INT NOT NULL,
    session_id VARCHAR(50) NOT NULL UNIQUE,
    location VARCHAR(100) DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_scan_time (scan_time),
    INDEX idx_session_id (session_id)
);

-- Tạo bảng face_data (dữ liệu chi tiết từng khuôn mặt)
CREATE TABLE IF NOT EXISTS face_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scan_id INT NOT NULL,
    face_number INT NOT NULL,
    age_group VARCHAR(50) NOT NULL,
    age_confidence FLOAT NOT NULL,
    face_width INT NOT NULL,
    face_height INT NOT NULL,
    face_area INT NOT NULL,
    position_x INT NOT NULL,
    position_y INT NOT NULL,
    texture_variance FLOAT NOT NULL,
    contrast_level FLOAT NOT NULL,
    edge_density FLOAT NOT NULL,
    smoothness FLOAT NOT NULL,
    face_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES face_scans(id) ON DELETE CASCADE,
    INDEX idx_scan_id (scan_id),
    INDEX idx_age_group (age_group),
    INDEX idx_face_hash (face_hash),
    INDEX idx_created_at (created_at)
);

-- Tạo view để xem thống kê nhanh
CREATE OR REPLACE VIEW face_statistics AS
SELECT 
    fs.scan_time,
    fs.location,
    fs.face_count,
    COUNT(fd.id) as processed_faces,
    GROUP_CONCAT(DISTINCT fd.age_group ORDER BY fd.age_group) as age_groups_found
FROM face_scans fs
LEFT JOIN face_data fd ON fs.id = fd.scan_id
GROUP BY fs.id
ORDER BY fs.scan_time DESC;

-- Tạo view thống kê theo nhóm tuổi
CREATE OR REPLACE VIEW age_group_stats AS
SELECT 
    age_group,
    COUNT(*) as total_count,
    AVG(age_confidence) as avg_confidence,
    AVG(face_area) as avg_face_size,
    MIN(created_at) as first_seen,
    MAX(created_at) as last_seen
FROM face_data
GROUP BY age_group
ORDER BY total_count DESC;

-- Tạo stored procedure để lấy thống kê theo ngày
DELIMITER //
CREATE PROCEDURE GetDailyStats(IN target_date DATE)
BEGIN
    SELECT 
        DATE(scan_time) as scan_date,
        COUNT(DISTINCT id) as total_scans,
        SUM(face_count) as total_faces,
        AVG(face_count) as avg_faces_per_scan
    FROM face_scans 
    WHERE DATE(scan_time) = target_date
    GROUP BY DATE(scan_time);
END //
DELIMITER ;

-- Tạo trigger để log các thay đổi
CREATE TABLE IF NOT EXISTS face_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id INT NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_operation (table_name, operation),
    INDEX idx_changed_at (changed_at)
);

-- Trigger cho face_scans
DELIMITER //
CREATE TRIGGER face_scans_audit 
AFTER INSERT ON face_scans
FOR EACH ROW
BEGIN
    INSERT INTO face_audit_log (table_name, operation, record_id, new_values)
    VALUES ('face_scans', 'INSERT', NEW.id, JSON_OBJECT(
        'scan_time', NEW.scan_time,
        'face_count', NEW.face_count,
        'session_id', NEW.session_id,
        'location', NEW.location
    ));
END //
DELIMITER ;

-- Tạo user cho ứng dụng (tùy chọn)
-- CREATE USER 'face_app'@'localhost' IDENTIFIED BY 'your_password_here';
-- GRANT SELECT, INSERT, UPDATE ON face_recognition.* TO 'face_app'@'localhost';
-- FLUSH PRIVILEGES;

-- Chèn dữ liệu mẫu (tùy chọn)
INSERT INTO face_scans (scan_time, face_count, session_id, location, notes) VALUES
('2025-01-20 10:00:00', 2, 'sample_20250120_100000', 'Văn phòng chính', 'Test dữ liệu mẫu'),
('2025-01-20 14:30:00', 1, 'sample_20250120_143000', 'Phòng họp A', 'Cuộc họp chiều');

-- Hiển thị thông tin đã tạo
SELECT 'Database và bảng đã được tạo thành công!' as status;
SELECT TABLE_NAME, TABLE_ROWS 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'face_recognition' 
AND TABLE_TYPE = 'BASE TABLE';

-- Hiển thị các view đã tạo
SELECT TABLE_NAME as view_name
FROM information_schema.VIEWS 
WHERE TABLE_SCHEMA = 'face_recognition';
