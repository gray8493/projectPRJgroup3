# Cafe POS System - Node.js + MySQL

## Cài đặt và chạy

### 1. Cài đặt Node.js
- Tải và cài Node.js từ: https://nodejs.org/
- Kiểm tra: `node --version` và `npm --version`

### 2. Cài đặt dependencies
```bash
npm install
```

### 3. Cấu hình database
- Tạo database `cafe_pos` trong MySQL
- Import file `table.sql` để tạo bảng và dữ liệu mẫu
- Cập nhật thông tin kết nối trong `server.js` (dòng 20-26):
  ```javascript
  const dbConfig = {
      host: 'localhost',
      port: 3306,
      user: 'root',
      password: 'your_password', // mật khẩu MySQL của bạn
      database: 'cafe_pos'
  };
  ```

### 4. Chạy server
```bash
# Chạy production
npm start

# Hoặc chạy development (tự động restart khi có thay đổi)
npm run dev
```

### 5. Truy cập ứng dụng
- Mở trình duyệt: http://localhost:3000
- API endpoints: http://localhost:3000/api/menu

## Tính năng
- ✅ Quản lý menu (Thêm/Sửa/Xóa)
- ✅ Đồng bộ real-time giữa quản lý và order
- ✅ Giỏ hàng và thanh toán
- ✅ Chọn bàn, loại đơn hàng
- ✅ Kết nối MySQL database

## API Endpoints
- `GET /api/health` - Kiểm tra kết nối database
- `GET /api/menu` - Lấy tất cả món
- `GET /api/menu?category=coffee` - Lấy món theo danh mục
- `POST /api/menu` - Thêm món mới
- `PUT /api/menu/:id` - Sửa món
- `DELETE /api/menu/:id` - Xóa món