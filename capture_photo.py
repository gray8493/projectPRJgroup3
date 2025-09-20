#!/usr/bin/env python3
"""
Script chụp ảnh nhanh và phân tích khuôn mặt
"""

import cv2
import os
from datetime import datetime

def capture_and_analyze():
    """Chụp ảnh và phân tích ngay lập tức"""
    print("📸 Chụp ảnh và Phân tích Khuôn mặt")
    print("=" * 40)
    
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Không thể mở camera!")
        return
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("✅ Camera và face detector đã sẵn sàng!")
    print("💡 Nhấn SPACE để chụp ảnh, ESC để thoát")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Phát hiện khuôn mặt real-time
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        
        # Vẽ khung khuôn mặt
        display_frame = frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display_frame, f'Face {len(faces)}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Hiển thị hướng dẫn
        cv2.putText(display_frame, f"Faces detected: {len(faces)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display_frame, "SPACE: Capture | ESC: Exit", (10, display_frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Capture Photo', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE key
            # Chụp ảnh
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            
            print(f"\n📸 Đã chụp ảnh: {filename}")
            
            # Phân tích ảnh vừa chụp
            analyze_photo(filename, face_cascade)
            
            # Hỏi có muốn chụp tiếp không
            choice = input("\n📷 Chụp ảnh khác? (y/n): ").strip().lower()
            if choice != 'y':
                break
                
        elif key == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()

def analyze_photo(filename, face_cascade):
    """Phân tích chi tiết ảnh đã chụp"""
    print(f"\n🔍 Phân tích ảnh: {filename}")
    
    # Đọc ảnh
    image = cv2.imread(filename)
    if image is None:
        print("❌ Không thể đọc ảnh!")
        return
    
    # Phát hiện khuôn mặt
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
    
    print(f"👥 Số khuôn mặt phát hiện: {len(faces)}")
    
    if len(faces) == 0:
        print("⚠️ Không phát hiện khuôn mặt nào!")
        return
    
    # Phân tích từng khuôn mặt
    for i, (x, y, w, h) in enumerate(faces):
        print(f"\n👤 Khuôn mặt {i+1}:")
        print(f"   📏 Vị trí: ({x}, {y})")
        print(f"   📐 Kích thước: {w}x{h} pixels")
        
        # Cắt vùng khuôn mặt
        face_region = image[y:y+h, x:x+w]
        
        # Phân tích cơ bản
        face_area = w * h
        if face_area < 5000:
            size_category = "Nhỏ (có thể là trẻ em)"
        elif face_area < 15000:
            size_category = "Trung bình"
        else:
            size_category = "Lớn (người lớn)"
        
        print(f"   📊 Diện tích: {face_area} pixels ({size_category})")
        
        # Lưu khuôn mặt riêng
        face_filename = f"face_{i+1}_{datetime.now().strftime('%H%M%S')}.jpg"
        cv2.imwrite(face_filename, face_region)
        print(f"   💾 Đã lưu khuôn mặt: {face_filename}")
    
    # Tạo ảnh kết quả với khung khuôn mặt
    result_image = image.copy()
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(result_image, f'Face {i+1}', (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Lưu ảnh kết quả
    result_filename = f"analyzed_{filename}"
    cv2.imwrite(result_filename, result_image)
    print(f"\n✅ Đã lưu ảnh phân tích: {result_filename}")
    
    # Hiển thị kết quả
    print("\n👁️ Hiển thị kết quả (nhấn phím bất kỳ để đóng)...")
    cv2.imshow('Analysis Result', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analyze_existing_photo():
    """Phân tích ảnh có sẵn"""
    print("\n📁 Phân tích ảnh có sẵn")
    
    # Liệt kê ảnh trong thư mục
    image_files = []
    for file in os.listdir('.'):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image_files.append(file)
    
    if image_files:
        print("\n📷 Ảnh có sẵn:")
        for i, file in enumerate(image_files):
            print(f"   {i+1}. {file}")
        
        try:
            choice = int(input(f"\nChọn ảnh (1-{len(image_files)}): ")) - 1
            if 0 <= choice < len(image_files):
                filename = image_files[choice]
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return
    else:
        filename = input("📷 Nhập đường dẫn ảnh: ").strip()
    
    if not os.path.exists(filename):
        print("❌ File không tồn tại!")
        return
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Phân tích
    analyze_photo(filename, face_cascade)

def main():
    print("🎯 Chụp ảnh và Phân tích Khuôn mặt")
    print("=" * 50)
    
    while True:
        print("\n📋 Chọn chế độ:")
        print("1. 📸 Chụp ảnh mới và phân tích")
        print("2. 📁 Phân tích ảnh có sẵn")
        print("3. ❌ Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (1-3): ").strip()
        
        if choice == '1':
            capture_and_analyze()
        elif choice == '2':
            analyze_existing_photo()
        elif choice == '3':
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
