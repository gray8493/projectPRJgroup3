# 🚀 Hướng dẫn Cài đặt Nhanh

## ⚠️ Lỗi "pip is not recognized" - KHẮC PHỤC NGAY

### Cách 1: Sử dụng python -m pip (Khuyến nghị)
```bash
python -m pip install -r requirements.txt
```

### Cách 2: Sử dụng py launcher
```bash
py -m pip install -r requirements.txt
```

### Cách 3: Kiểm tra Python đã cài đặt chưa
```bash
python --version
py --version
```

## Bước 1: Cài đặt Python (Nếu chưa có)

### 🚀 Cách nhanh nhất - Chạy script tự động:
```bash
install_python.bat
```

### 📋 Cách thủ công:

#### Phương pháp A: Từ python.org (Khuyến nghị)
1. Truy cập [python.org/downloads](https://python.org/downloads)
2. Tải Python 3.8+ (phiên bản mới nhất)
3. **⚠️ QUAN TRỌNG**: Tick vào "Add Python to PATH" khi cài đặt
4. Cài đặt với quyền Administrator
5. Restart Command Prompt sau khi cài đặt

#### Phương pháp B: Từ Microsoft Store
1. Mở Microsoft Store
2. Tìm kiếm "Python"
3. Cài đặt Python từ Microsoft
4. Restart Command Prompt

### ✅ Kiểm tra cài đặt thành công:
```bash
python --version
# Hoặc
py --version
```

## Bước 2: Cài đặt thư viện

### Phương pháp A: Cài đặt từng thư viện
```bash
python -m pip install opencv-python==4.8.1.78
python -m pip install numpy==1.24.3
python -m pip install streamlit==1.28.1
python -m pip install Pillow==10.0.0
python -m pip install matplotlib==3.7.2
```

### Phương pháp B: Cài đặt tất cả cùng lúc
```bash
python -m pip install -r requirements.txt
```

## Bước 3: Test cài đặt
```bash
python demo.py
```

## Bước 4: Chạy ứng dụng

### Giao diện Web (Streamlit):
```bash
streamlit run simple_face_age_app.py
```

### Console Application:
```bash
python opencv_face_age.py
```

### Windows Batch File:
Double-click vào `run_app.bat`

## Xử lý lỗi thường gặp

### Lỗi OpenCV:
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

### Lỗi Camera:
- Kiểm tra camera có hoạt động không
- Đóng các ứng dụng khác đang sử dụng camera
- Chạy với quyền Administrator

### Lỗi Streamlit:
```bash
pip install --upgrade streamlit
```

## Kiểm tra hệ thống
```python
import cv2
print("OpenCV version:", cv2.__version__)

# Test camera
cap = cv2.VideoCapture(0)
print("Camera OK:", cap.isOpened())
cap.release()
```
