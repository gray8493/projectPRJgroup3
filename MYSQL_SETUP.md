# 🗄️ Hướng dẫn Cài đặt MySQL cho Hệ thống Quét Khuôn mặt

## 📋 Yêu cầu
- Windows 10/11
- Python đã cài đặt
- Quyền Administrator

## 🚀 Bước 1: Cài đặt MySQL Server

### Phương pháp A: MySQL Installer (Khuyến nghị)
1. Truy cập [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
2. Tải **MySQL Installer for Windows**
3. Chạy file installer với quyền Administrator
4. Chọn **Developer Default** hoặc **Server only**
5. Thiết lập mật khẩu root (ghi nhớ mật khẩu này!)
6. Hoàn thành cài đặt

### Phương pháp B: XAMPP (Dễ dàng hơn)
1. Tải [XAMPP](https://www.apachefriends.org/download.html)
2. Cài đặt XAMPP
3. Khởi động **Apache** và **MySQL** trong XAMPP Control Panel
4. Mật khẩu root mặc định là rỗng

## 🔧 Bước 2: Cài đặt Python MySQL Connector

```bash
py -m pip install mysql-connector-python
```

## 🗄️ Bước 3: Tạo Database

### Cách 1: Sử dụng MySQL Command Line
```bash
mysql -u root -p
```

Sau đó chạy:
```sql
CREATE DATABASE face_recognition;
USE face_recognition;
source setup_database.sql
```

### Cách 2: Sử dụng phpMyAdmin (nếu dùng XAMPP)
1. Mở trình duyệt: `http://localhost/phpmyadmin`
2. Tạo database mới tên `face_recognition`
3. Import file `setup_database.sql`

### Cách 3: Sử dụng MySQL Workbench
1. Mở MySQL Workbench
2. Kết nối đến MySQL Server
3. Mở file `setup_database.sql`
4. Chạy script

## ⚙️ Bước 4: Cấu hình Kết nối

Khi chạy ứng dụng, bạn sẽ được hỏi:

```
🌐 MySQL Host (localhost): localhost
👤 MySQL User (root): root
🔐 MySQL Password: [nhập mật khẩu của bạn]
🗄️ Database name (face_recognition): face_recognition
```

## 🎯 Bước 5: Chạy Ứng dụng

```bash
py face_to_database.py
```

## 📊 Cấu trúc Database

### Bảng `face_scans`
- `id`: ID tự động tăng
- `scan_time`: Thời gian quét
- `face_count`: Số khuôn mặt phát hiện
- `session_id`: ID phiên quét
- `location`: Vị trí quét
- `notes`: Ghi chú

### Bảng `face_data`
- `id`: ID tự động tăng
- `scan_id`: Liên kết đến face_scans
- `face_number`: Số thứ tự khuôn mặt
- `age_group`: Nhóm tuổi ước tính
- `age_confidence`: Độ tin cậy (0-1)
- `face_width`, `face_height`: Kích thước khuôn mặt
- `face_area`: Diện tích khuôn mặt
- `position_x`, `position_y`: Vị trí trong ảnh
- `texture_variance`: Độ nhám da
- `contrast_level`: Độ tương phản
- `edge_density`: Mật độ cạnh
- `smoothness`: Độ mịn
- `face_hash`: Hash để tránh trùng lặp

## 🔍 Truy vấn Dữ liệu Hữu ích

### Xem tất cả lần quét:
```sql
SELECT * FROM face_scans ORDER BY scan_time DESC;
```

### Thống kê theo nhóm tuổi:
```sql
SELECT age_group, COUNT(*) as count 
FROM face_data 
GROUP BY age_group 
ORDER BY count DESC;
```

### Xem chi tiết một lần quét:
```sql
SELECT fs.*, fd.age_group, fd.age_confidence
FROM face_scans fs
JOIN face_data fd ON fs.id = fd.scan_id
WHERE fs.session_id = 'YOUR_SESSION_ID';
```

### Thống kê theo ngày:
```sql
SELECT DATE(scan_time) as date, 
       COUNT(*) as scans, 
       SUM(face_count) as total_faces
FROM face_scans 
GROUP BY DATE(scan_time)
ORDER BY date DESC;
```

## 🛠️ Xử lý Sự cố

### Lỗi "Access denied for user 'root'"
- Kiểm tra mật khẩu MySQL
- Đảm bảo MySQL Server đang chạy

### Lỗi "Can't connect to MySQL server"
- Kiểm tra MySQL Service đang chạy
- Kiểm tra port 3306 không bị chặn

### Lỗi "Database doesn't exist"
- Chạy lại script `setup_database.sql`
- Tạo database thủ công

### Lỗi "Table doesn't exist"
- Import lại file `setup_database.sql`
- Kiểm tra quyền user

## 📈 Tối ưu Performance

### Tạo index cho truy vấn nhanh:
```sql
CREATE INDEX idx_scan_time ON face_scans(scan_time);
CREATE INDEX idx_age_group ON face_data(age_group);
CREATE INDEX idx_face_hash ON face_data(face_hash);
```

### Backup dữ liệu:
```bash
mysqldump -u root -p face_recognition > backup.sql
```

### Restore dữ liệu:
```bash
mysql -u root -p face_recognition < backup.sql
```

## 🔒 Bảo mật

1. **Đổi mật khẩu root mạnh**
2. **Tạo user riêng cho ứng dụng**
3. **Giới hạn quyền truy cập**
4. **Backup định kỳ**

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra MySQL Service đang chạy
2. Kiểm tra firewall không chặn port 3306
3. Xem log lỗi trong MySQL error log
4. Kiểm tra quyền user và database

---

**Lưu ý**: Hệ thống này chỉ lưu dữ liệu phân tích, không lưu ảnh gốc để bảo vệ quyền riêng tư.
