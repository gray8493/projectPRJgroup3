# ☕ Coffee Shop Management System

Hệ thống quản lý quán cà phê hiện đại với giao diện admin và staff, tích hợp bảo mật phân quyền người dùng.

## 🚀 Tính năng chính

### 🔐 Hệ thống xác thực & phân quyền
- **Đăng nhập bảo mật** với phân quyền dựa trên vai trò
- **Hai loại tài khoản**:
  - **👨‍💼 Admin**: Toàn quyền truy cập tất cả chức năng
  - **👩‍💻 Staff**: Chỉ truy cập menu và quản lý đơn hàng

### 🎛️ Trang quản trị Admin (`/index.html`)
- ✅ Quản lý menu cà phê hoàn chỉnh
- ➕ Thêm, sửa, xóa sản phẩm cà phê
- 📝 Quản lý thông tin sản phẩm:
  - Tên sản phẩm
  - Mô tả chi tiết
  - Giá bán
  - Danh mục
  - Trạng thái có sẵn

### 🍽️ Giao diện Menu (`/menu.html`)
- 🎨 Giao diện lưới đẹp mắt hiển thị sản phẩm
- 🛒 Giỏ hàng tương tác
- 💰 Cập nhật giá real-time
- 🔍 Lọc theo danh mục
- 📱 Thiết kế responsive cho mọi thiết bị
- ⚙️ Tùy chỉnh đơn hàng (hương vị, nhiệt độ)
- 🏪 Chọn loại đơn hàng (Dine In, Take Away, Delivery)

## 🛠️ Công nghệ sử dụng

### Backend
- ☕ **Java 21**
- 🌱 **Spring Boot 2.7.18**
- 🔒 **Spring Security** - Bảo mật & phân quyền
- 🗄️ **Spring Data JPA** - ORM
- 🐬 **MySQL 8.x** - Cơ sở dữ liệu
- 📦 **Maven** - Quản lý dependencies

### Frontend
- 🌐 **HTML5**
- 🎨 **CSS3** với Tailwind CSS
- ⚡ **JavaScript ES6+**
- 🎯 **Font Awesome Icons**
- 📱 **Responsive Design**

## 📁 Cấu trúc dự án

```
projectPRJgroup3-main/
├── src/
│   ├── main/
│   │   ├── java/com/coffeeshop/
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java      # Cấu hình bảo mật
│   │   │   │   └── WebConfig.java           # Cấu hình web
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java      # API xác thực
│   │   │   │   ├── CoffeeController.java    # API quản lý cà phê
│   │   │   │   └── TestController.java
│   │   │   ├── model/
│   │   │   │   ├── Coffee.java              # Entity cà phê
│   │   │   │   └── User.java                # Entity người dùng
│   │   │   ├── repository/
│   │   │   │   ├── CoffeeRepository.java
│   │   │   │   └── UserRepository.java
│   │   │   ├── service/
│   │   │   │   ├── CustomUserDetailsService.java
│   │   │   │   └── DataInitializationService.java
│   │   │   └── CoffeeShopApplication.java
│   │   └── resources/
│   │       ├── static/
│   │       │   ├── index.html               # Trang admin
│   │       │   ├── login.html               # Trang đăng nhập
│   │       │   ├── menu.html                # Trang menu
│   │       │   ├── display.html
│   │       │   └── test-api.html
│   │       └── application.properties
├── pom.xml
└── README.md
```

## 🚀 Hướng dẫn cài đặt

### 📋 Yêu cầu hệ thống
- ☕ **Java Development Kit (JDK) 21**
- 📦 **Maven 3.8.x** trở lên
- 🐬 **MySQL 8.x**

### 🔧 Cài đặt

1. **Clone repository:**
```bash
git clone [repository-url]
cd projectPRJgroup3-main
```

2. **Cấu hình database trong `application.properties`:**
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/coffeeshop
spring.datasource.username=your_username
spring.datasource.password=your_password
spring.jpa.hibernate.ddl-auto=update
```

3. **Tạo database:**
```sql
CREATE DATABASE coffeeshop;
```

4. **Build project:**
```bash
mvn clean install
```

5. **Chạy ứng dụng:**
```bash
mvn spring-boot:run
```

6. **Truy cập ứng dụng:**
- Mở trình duyệt và vào `http://localhost:8083`
- Bạn sẽ được chuyển hướng đến trang đăng nhập

### 🔑 Tài khoản mặc định

#### 👨‍💼 Tài khoản Admin:
- **Username:** `admin`
- **Password:** `admin123`
- **Quyền truy cập:** Trang admin + menu + tất cả API

#### 👩‍💻 Tài khoản Staff:
- **Username:** `staff`
- **Password:** `staff123`
- **Quyền truy cập:** Chỉ trang menu + API đọc dữ liệu

## 🔒 Tính năng bảo mật

- 🛡️ **Phân quyền dựa trên vai trò (RBAC)**
- ✅ **Xác thực session-based**
- 🔐 **Mã hóa mật khẩu BCrypt**
- 🚫 **Bảo vệ routes frontend**
- 🔒 **Bảo vệ API endpoints**
- 🚪 **Tự động logout**
- 🛡️ **CSRF protection**

## 📡 API Endpoints

### 🔐 Authentication
- `POST /api/auth/login` - Đăng nhập
- `POST /api/auth/logout` - Đăng xuất
- `GET /api/auth/user` - Lấy thông tin user hiện tại

### ☕ Coffee Management
- `GET /api/coffees` - Lấy danh sách cà phê *(ADMIN + STAFF)*
- `GET /api/coffees/{id}` - Lấy chi tiết cà phê *(ADMIN + STAFF)*
- `POST /api/coffees` - Thêm cà phê mới *(ADMIN only)*
- `PUT /api/coffees/{id}` - Cập nhật cà phê *(ADMIN only)*
- `DELETE /api/coffees/{id}` - Xóa cà phê *(ADMIN only)*

## 🎯 Luồng hoạt động

### 🔄 Đăng nhập với Admin:
1. Vào `/login.html`
2. Nhập `admin` / `admin123`
3. Redirect đến `/index.html` (trang quản trị)
4. Có thể vào menu và quay lại admin
5. Có thể thực hiện tất cả CRUD operations

### 🔄 Đăng nhập với Staff:
1. Vào `/login.html`
2. Nhập `staff` / `staff123`
3. Redirect đến `/menu.html` (trang menu)
4. Chỉ có thể sử dụng menu ordering
5. Không thể truy cập trang admin
6. Nút "Quay lại Admin" bị ẩn

## 🚀 Tính năng nâng cao

- 🎨 **Giao diện đẹp mắt** với Tailwind CSS
- 📱 **Responsive design** cho mobile
- ⚡ **Real-time updates**
- 🛒 **Shopping cart functionality**
- 🎛️ **Order customization** (flavor, temperature)
- 🏪 **Multiple order types** (Dine In, Take Away, Delivery)
- 👥 **Customer display mode**

## 🔮 Tính năng tương lai

1. 📊 **Hệ thống báo cáo & thống kê**
2. 💳 **Tích hợp thanh toán**
3. 🎁 **Chương trình khách hàng thân thiết**
4. 📦 **Quản lý kho hàng**
5. 👥 **Quản lý nhân viên & ca làm việc**
6. 📱 **Mobile app**
7. 🔔 **Push notifications**

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được cấp phép theo MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

**Phát triển bởi:** Nhóm 3 - Coffee Shop Management System  
**Phiên bản:** 1.0.0  
**Cập nhật cuối:** 2025-01-01