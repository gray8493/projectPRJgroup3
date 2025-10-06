# POS Cafe - Hệ thống quản lý quán cà phê đa chi nhánh

## 📋 Mô tả
Hệ thống POS (Point of Sale) hiện đại cho chuỗi quán cà phê với khả năng quản lý đa chi nhánh, menu riêng biệt và hệ thống phân quyền hoàn chỉnh.

## ✨ Tính năng chính

### 🏪 Quản lý đa chi nhánh
- **Chọn quán**: Mỗi quán có menu và dữ liệu riêng biệt
- **Menu độc lập**: Admin chỉ quản lý menu của quán hiện tại
- **Thông tin quán**: Hiển thị tên và địa chỉ quán trên giao diện

### 🔐 Hệ thống đăng nhập & phân quyền
- **Đăng ký tài khoản**: Nhân viên có thể tự đăng ký tài khoản
- **Phân quyền**: Admin và Staff với quyền hạn khác nhau
- **Bảo mật**: Yêu cầu đăng nhập để truy cập menu

### 📱 Menu khách hàng thông minh
- **Gợi ý theo tuổi**: AI nhận diện tuổi và gợi ý thức uống phù hợp
- **Chọn size**: S, M, L, XL với giá khác nhau
- **Topping**: Trân châu, thạch, kem cheese
- **Ghi chú**: Khách hàng có thể ghi chú đặc biệt
- **Giỏ hàng**: Quản lý đơn hàng trực quan

### 💳 Thanh toán QR
- **QR Code**: Tự động tạo mã QR thanh toán
- **Thông tin đầy đủ**: Hiển thị chi tiết đơn hàng với size, topping, note
- **Feedback**: Khách hàng có thể để lại đánh giá

### ⚙️ Admin Panel nâng cao
- **4 Tab chức năng**:
  - 📝 **Thêm món**: Quản lý menu theo danh mục
  - 📊 **Doanh thu**: Thống kê theo ngày
  - 👥 **Hội viên**: Quản lý khách hàng thân thiết
  - 📋 **Lịch sử đơn hàng**: Theo dõi các đơn đã hoàn thành

## 🚀 Cách chạy trên localhost

### Phương pháp 1: Sử dụng Python (Khuyến nghị)
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Sau đó mở trình duyệt và truy cập: `http://localhost:8000`

### Phương pháp 2: Sử dụng Node.js
```bash
# Cài đặt http-server globally
npm install -g http-server

# Chạy server
http-server -p 8000
```

### Phương pháp 3: Sử dụng Live Server (VS Code)
1. Cài đặt extension "Live Server" trong VS Code
2. Click chuột phải vào file `store-selection.html`
3. Chọn "Open with Live Server"

## 📁 Cấu trúc thư mục
```
prj_fe/
├── store-selection.html   # Trang chọn quán và đăng nhập
├── login.html             # Trang đăng ký tài khoản
├── menu.html              # Menu khách hàng
├── customer.html           # Trang thanh toán QR
├── admin.html              # Panel quản trị
├── assets/
│   └── css/
│       └── style.css       # File CSS chính
└── README.md              # Hướng dẫn này
```

## 🎯 Hướng dẫn sử dụng

### 1. Bắt đầu
- Truy cập `store-selection.html` để chọn quán và đăng nhập
- Hoặc vào `login.html` để đăng ký tài khoản mới

### 2. Đăng nhập hệ thống
- **Admin mặc định**: `admin` / `123456`
- **Nhân viên mới**: Đăng ký tại `login.html`
- **Chọn quán**: Mỗi quán có menu riêng biệt

### 3. Sử dụng menu khách hàng
- **Gợi ý tuổi**: Hệ thống sẽ hỏi tuổi để gợi ý thức uống
- **Chọn sản phẩm**: Cà phê, trà trái cây, trà sữa, đồ ăn
- **Tùy chỉnh**: Chọn size, topping, ghi chú
- **Thanh toán**: Quét QR để thanh toán

### 4. Quản lý admin
- **Thêm món**: Quản lý menu theo danh mục
- **Xem doanh thu**: Thống kê theo ngày
- **Quản lý hội viên**: Thông tin khách hàng thân thiết
- **Lịch sử đơn hàng**: Theo dõi các đơn đã hoàn thành

## 🎨 Thiết kế & Giao diện

### Màu sắc
- **Tông màu chính**: Dark theme với điểm nhấn vàng cam (#f59e0b)
- **Màu phụ**: Tím (#8b5cf6) và xanh cyan (#06b6d4)
- **Gradient**: Hiệu ứng gradient đẹp mắt
- **Shadow**: Box shadow mềm mại

### Responsive Design
- **Mobile-first**: Tối ưu cho điện thoại
- **Tablet**: Giao diện thích ứng cho máy tính bảng
- **Desktop**: Trải nghiệm đầy đủ trên máy tính

### UI Components
- **Tabs**: Giao diện tab hiện đại
- **Cards**: Card design với hover effects
- **Buttons**: Button với gradient và animation
- **Forms**: Input fields với focus effects

## 🔧 Công nghệ sử dụng

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Flexbox, Grid, Custom Properties
- **JavaScript ES6+**: Modern JavaScript features
- **LocalStorage**: Lưu trữ dữ liệu local
- **SessionStorage**: Quản lý phiên đăng nhập

### Tính năng đặc biệt
- **AI Age Detection**: Mô phỏng nhận diện tuổi
- **QR Code Generation**: Tạo mã QR động
- **Multi-store Management**: Quản lý đa chi nhánh
- **Real-time Cart**: Giỏ hàng cập nhật real-time

## 📊 Dữ liệu mẫu

### Quán có sẵn
- **Quán Cà Phê ABC - Quận 1**
- **Quán Cà Phê XYZ - Quận 3**
- **Quán Cà Phê DEF - Quận 7**

### Menu mặc định
- **Cà phê**: Đen, sữa, bạc xỉu, latte
- **Trà trái cây**: Đào, vải, chanh, cam
- **Trà sữa**: Truyền thống, matcha, socola, thái
- **Đồ ăn**: Sandwich, bánh ngọt, bánh kem, bánh quy

## ⚙️ Tùy chỉnh

### Thêm quán mới
```javascript
// Trong store-selection.html
const stores = {
  'store4': {
    id: 'store4',
    name: 'Tên quán mới',
    address: 'Địa chỉ quán',
    phone: 'Số điện thoại'
  }
};
```

### Thêm sản phẩm
```javascript
// Trong admin.html hoặc menu.html
const newItem = {
  id: 'unique_id',
  name: 'Tên sản phẩm',
  price: 25000,
  img: 'url_hình_ảnh'
};
```

### Thay đổi màu sắc
```css
/* Trong assets/css/style.css */
:root {
  --color-primary: #your-color;
  --color-secondary: #your-color;
}
```

## 🐛 Xử lý lỗi

### Lỗi thường gặp
1. **Không load được CSS**: Kiểm tra đường dẫn file
2. **JavaScript error**: Mở Console để xem lỗi
3. **LocalStorage**: Kiểm tra trình duyệt có hỗ trợ không
4. **QR Code**: Cần kết nối internet để tạo QR

### Debug
```javascript
// Kiểm tra dữ liệu localStorage
console.log(localStorage.getItem('stores'));
console.log(localStorage.getItem('storeMenus'));
console.log(sessionStorage.getItem('currentStore'));
```

## 📈 Tính năng nâng cao

### AI & Machine Learning
- **Age Detection**: Nhận diện tuổi từ camera
- **Recommendation**: Gợi ý sản phẩm thông minh
- **Analytics**: Phân tích hành vi khách hàng

### Multi-language Support
- **Tiếng Việt**: Giao diện chính
- **English**: Có thể mở rộng
- **i18n**: Hỗ trợ đa ngôn ngữ

### Integration Ready
- **Payment Gateway**: Tích hợp cổng thanh toán
- **Inventory Management**: Quản lý kho
- **CRM**: Quản lý khách hàng
- **Reporting**: Báo cáo chi tiết

## 🤝 Đóng góp

### Cách đóng góp
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

### Guidelines
- Code style: ESLint + Prettier
- Commit message: Conventional Commits
- Testing: Manual testing required
- Documentation: Update README

## 📄 License
MIT License - Xem file LICENSE để biết thêm chi tiết

## 📞 Hỗ trợ
- **Email**: support@poscafe.com
- **Documentation**: [Wiki](https://github.com/poscafe/wiki)
- **Issues**: [GitHub Issues](https://github.com/poscafe/issues)

---

**POS Cafe** - Hệ thống quản lý quán cà phê đa chi nhánh hiện đại 🚀☕

*Phiên bản 2.0 - Multi-store Management System*