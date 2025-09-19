# Hướng dẫn cài đặt và chạy hệ thống POS Cafe

## 1. Cài đặt Database MySQL

1. Cài đặt MySQL Server trên máy tính
2. Tạo database và import file `db.sql`:
   ```sql
   mysql -u root -p < db.sql
   ```

## 2. Cấu hình Database

Tạo file `.env` trong thư mục gốc với nội dung:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=anhthi060105
DB_NAME=cafe_pos
PORT=3000
```

**Lưu ý:** Thay đổi `DB_PASSWORD` thành mật khẩu MySQL của bạn.

## 3. Cài đặt và chạy ứng dụng

1. Cài đặt dependencies:
   ```bash
   npm install
   ```

2. Chạy server:
   ```bash
   npm start
   ```

3. Mở trình duyệt và truy cập: `http://localhost:3000`

## 4. Sử dụng hệ thống

1. **Tạo món ăn mới:**
   - Điền thông tin món ăn trong form "Quản lý menu"
   - Nhấn "Lưu" để lưu vào database
   - Món ăn sẽ xuất hiện trong danh sách và có thể thêm vào đơn hàng

2. **Đặt hàng:**
   - Chọn loại đơn hàng (Tại chỗ/Mang về/Giao hàng)
   - Nếu chọn "Tại chỗ", chọn bàn
   - Click vào món ăn để thêm vào giỏ hàng
   - Nhấn "Thanh toán" để hoàn tất đơn hàng

## 5. API Endpoints

- `GET /api/health` - Kiểm tra trạng thái server
- `GET /api/menu` - Lấy tất cả món ăn
- `GET /api/menu?category=coffee` - Lấy món ăn theo danh mục
- `POST /api/menu` - Tạo món ăn mới
- `PUT /api/menu/:id` - Cập nhật món ăn
- `DELETE /api/menu/:id` - Xóa món ăn

## Khắc phục sự cố

Nếu gặp lỗi kết nối database:
1. Kiểm tra MySQL đã chạy chưa
2. Kiểm tra thông tin trong file `.env`
3. Kiểm tra database `cafe_pos` đã được tạo chưa
4. Kiểm tra bảng `menu_items` đã có dữ liệu chưa
