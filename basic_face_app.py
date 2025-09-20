#!/usr/bin/env python3
"""
Ứng dụng nhận diện khuôn mặt cơ bản - chỉ cần OpenCV
"""

import cv2
import os
from datetime import datetime

def main():
    print("🎯 Ứng dụng Nhận diện Khuôn mặt Cơ bản")
    print("=" * 50)
    
    # Kiểm tra OpenCV
    try:
        print(f"OpenCV version: {cv2.__version__}")
    except:
        print("❌ OpenCV chưa được cài đặt!")
        print("Chạy: py -m pip install opencv-python")
        return
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("❌ Không thể load face detector!")
        return
    
    print("✅ Face detector đã sẵn sàng!")
    
    while True:
        print("\n📋 Chọn chế độ:")
        print("1. 📹 Camera trực tiếp")
        print("2. 📷 Phân tích ảnh")
        print("3. ❌ Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (1-3): ").strip()
        
        if choice == '1':
            camera_mode(face_cascade)
        elif choice == '2':
            image_mode(face_cascade)
        elif choice == '3':
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

def camera_mode(face_cascade):
    """Chế độ camera trực tiếp"""
    print("\n📹 Khởi động camera...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Không thể mở camera!")
        return
    
    print("✅ Camera đã sẵn sàng!")
    print("💡 Nhấn 'q' để thoát, 's' để chụp ảnh")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Không thể đọc frame!")
            break
        
        # Phát hiện khuôn mặt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        
        # Vẽ khung khuôn mặt
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face Detected', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Hiển thị thông tin
        info = f"Faces: {len(faces)}"
        cv2.putText(frame, info, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, "Press 'q' to quit, 's' to save", (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Hiển thị frame
        cv2.imshow('Face Detection', frame)
        
        # Xử lý phím
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Lưu ảnh
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Đã lưu ảnh: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()

def image_mode(face_cascade):
    """Chế độ phân tích ảnh"""
    image_path = input("\n📷 Nhập đường dẫn ảnh: ").strip()
    
    if not os.path.exists(image_path):
        print("❌ File không tồn tại!")
        return
    
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Không thể đọc ảnh!")
        return
    
    print("🔄 Đang phân tích...")
    
    # Phát hiện khuôn mặt
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
    
    # Vẽ kết quả
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, 'Face', (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Hiển thị kết quả
    print(f"\n✅ Phát hiện {len(faces)} khuôn mặt!")
    
    # Hiển thị ảnh
    cv2.imshow('Result', image)
    print("\n💡 Nhấn phím bất kỳ để tiếp tục...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Lưu kết quả
    save = input("💾 Lưu kết quả? (y/n): ").strip().lower()
    if save == 'y':
        output_path = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(output_path, image)
        print(f"✅ Đã lưu: {output_path}")

if __name__ == "__main__":
    main()
