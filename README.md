# 🎯 Ứng dụng Nhận diện Khuôn mặt và Ước tính Độ tuổi

Ứng dụng sử dụng OpenCV và Computer Vision để phát hiện khuôn mặt và ước tính độ tuổi từ camera hoặc ảnh.

## 🚀 Tính năng

- ✅ **Phát hiện khuôn mặt**: Sử dụng Haar Cascades của OpenCV
- ✅ **Ước tính độ tuổi**: Phân tích đặc trưng khuôn mặt để ước tính nhóm tuổi
- ✅ **Camera trực tiếp**: Phân tích real-time từ webcam
- ✅ **Phân tích ảnh**: Upload và phân tích ảnh có sẵn
- ✅ **Giao diện web**: Sử dụng Streamlit (tùy chọn)
- ✅ **Giao diện console**: Chạy trực tiếp với OpenCV

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Webcam (cho chế độ camera trực tiếp)
- Windows/macOS/Linux

## 🛠️ Cài đặt

### 1. Clone hoặc tải xuống dự án

```bash
git clone <repository-url>
cd face-age-detection
```

### 2. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 3. Kiểm tra cài đặt

```python
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

## 🎮 Cách sử dụng

### Phiên bản 1: Giao diện Web (Streamlit)

```bash
streamlit run simple_face_age_app.py
```

**Tính năng:**
- 📤 Tải ảnh lên
- 📸 Chụp ảnh trực tiếp
- 📹 Camera trực tiếp (local)
- 🎨 Giao diện đẹp, dễ sử dụng

### Phiên bản 2: Console Application

```bash
python opencv_face_age.py
```

**Tính năng:**
- 📹 Camera trực tiếp với hiển thị real-time
- 📷 Phân tích ảnh đơn lẻ
- 📁 Phân tích hàng loạt ảnh trong thư mục
- 📊 Thống kê chi tiết

### Phiên bản 3: Advanced (với AI Models)

```bash
streamlit run face_age_detector.py
```

**Lưu ý:** Cần tải xuống các model AI (sẽ tự động tải khi chạy lần đầu)

## 📊 Nhóm tuổi được phân loại

| Nhóm | Độ tuổi | Màu hiển thị |
|------|---------|--------------|
| 👶 Trẻ em | 0-12 tuổi | Magenta |
| 🧒 Thiếu niên | 13-19 tuổi | Cyan |
| 👨 Thanh niên | 20-35 tuổi | Green |
| 👨‍💼 Trung niên | 36-55 tuổi | Yellow |
| 👴 Cao tuổi | 56+ tuổi | Red |

## 🔧 Cấu hình

### Tùy chỉnh độ nhạy phát hiện khuôn mặt

Trong file `opencv_face_age.py`, tìm và chỉnh sửa:

```python
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,      # Tăng để phát hiện nhanh hơn
    minNeighbors=5,       # Tăng để giảm false positive
    minSize=(50, 50),     # Kích thước khuôn mặt tối thiểu
)
```

### Tùy chỉnh thuật toán ước tính tuổi

Chỉnh sửa hàm `estimate_age_group()` để điều chỉnh logic phân loại.

## 📁 Cấu trúc dự án

```
face-age-detection/
├── requirements.txt              # Danh sách thư viện
├── README.md                    # Hướng dẫn này
├── simple_face_age_app.py       # Ứng dụng Streamlit đơn giản
├── opencv_face_age.py           # Ứng dụng console OpenCV
├── face_age_detector.py         # Phiên bản advanced với AI
└── models/                      # Thư mục chứa AI models (tự động tạo)
```

## 🎯 Hướng dẫn sử dụng chi tiết

### 1. Camera trực tiếp

1. Chạy ứng dụng
2. Chọn chế độ "Camera trực tiếp"
3. Cho phép truy cập camera
4. Khuôn mặt sẽ được phát hiện và hiển thị độ tuổi real-time

**Phím tắt:**
- `q`: Thoát camera
- `s`: Chụp và lưu ảnh

### 2. Phân tích ảnh

1. Chọn chế độ "Phân tích ảnh"
2. Nhập đường dẫn file ảnh
3. Xem kết quả phân tích
4. Lưu kết quả nếu muốn

### 3. Phân tích hàng loạt

1. Chọn chế độ "Phân tích thư mục"
2. Nhập đường dẫn thư mục chứa ảnh
3. Ứng dụng sẽ xử lý tất cả ảnh
4. Xem thống kê tổng quan

## 🔍 Cách thức hoạt động

### Phát hiện khuôn mặt
- Sử dụng **Haar Cascades** của OpenCV
- Chuyển ảnh sang grayscale
- Quét ảnh với các scale khác nhau
- Trả về tọa độ các khuôn mặt

### Ước tính độ tuổi
Phân tích các đặc trưng:

1. **Texture Analysis**: Độ nhám của da
   - Da mịn → Trẻ
   - Da nhăn → Già

2. **Contrast Analysis**: Độ tương phản
   - Tương phản cao → Trẻ
   - Tương phản thấp → Già

3. **Edge Density**: Mật độ cạnh (nếp nhăn)
   - Ít cạnh → Trẻ
   - Nhiều cạnh → Già

4. **Face Size**: Kích thước khuôn mặt
   - Nhỏ → Trẻ em
   - Lớn → Người lớn

## ⚠️ Lưu ý quan trọng

### Độ chính xác
- Đây là ước tính cơ bản, không phải chẩn đoán chính xác
- Độ chính xác phụ thuộc vào chất lượng ảnh
- Ánh sáng và góc chụp ảnh hưởng đến kết quả

### Quyền riêng tư
- Ứng dụng không lưu trữ dữ liệu cá nhân
- Chỉ xử lý local trên máy tính
- Không gửi ảnh lên internet

### Hiệu năng
- Camera 720p: ~15-20 FPS
- Ảnh 1080p: ~1-2 giây xử lý
- CPU usage: 20-40%

## 🐛 Xử lý sự cố

### Camera không hoạt động
```bash
# Kiểm tra camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

### Lỗi import OpenCV
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

### Streamlit không chạy
```bash
pip install --upgrade streamlit
streamlit --version
```

## 🔄 Cập nhật và phát triển

### Cải thiện độ chính xác
1. Thêm nhiều đặc trưng phân tích
2. Sử dụng machine learning models
3. Training với dataset lớn hơn

### Tính năng mới
- [ ] Nhận diện giới tính
- [ ] Phát hiện cảm xúc
- [ ] Lưu lịch sử phân tích
- [ ] Export báo cáo

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra requirements.txt
2. Đảm bảo camera hoạt động
3. Kiểm tra phiên bản Python
4. Xem log lỗi chi tiết

## 📄 License

MIT License - Sử dụng tự do cho mục đích học tập và nghiên cứu.

## 🙏 Tài liệu tham khảo

- [OpenCV Documentation](https://docs.opencv.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Haar Cascades](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)

---

**Tác giả**: AI Assistant  
**Ngày tạo**: 2025  
**Phiên bản**: 1.0
