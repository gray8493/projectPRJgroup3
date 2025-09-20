#!/usr/bin/env python3
"""
Test nhanh phân tích tuổi - phiên bản đơn giản
"""

import cv2
import numpy as np

def quick_age_estimate(face_width, face_height, face_area):
    """Ước tính tuổi đơn giản dựa trên kích thước"""
    
    if face_area < 4000:
        return "Trẻ em (0-12 tuổi)", (255, 255, 0)
    elif face_area < 8000:
        return "Thiếu niên (13-17 tuổi)", (0, 255, 255)  
    elif face_area < 15000:
        return "Thanh niên (18-30 tuổi)", (0, 255, 0)
    elif face_area < 25000:
        return "Trung niên (31-50 tuổi)", (255, 165, 0)
    else:
        return "Cao tuổi (50+ tuổi)", (0, 0, 255)

def main():
    print("🎯 Test Nhanh Phân tích Tuổi")
    print("=" * 40)
    
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Không thể mở camera!")
        return
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("✅ Camera và face detector đã sẵn sàng!")
    print("💡 Nhấn SPACE để phân tích, ESC để thoát")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Phát hiện khuôn mặt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        
        # Xử lý từng khuôn mặt
        for i, (x, y, w, h) in enumerate(faces):
            # Tính diện tích
            face_area = w * h
            
            # Ước tính tuổi
            age_estimate, color = quick_age_estimate(w, h, face_area)
            
            # Vẽ khung khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Vẽ thông tin tuổi
            cv2.putText(frame, age_estimate, (x, y-30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Vẽ thông tin kích thước
            size_info = f"Size: {w}x{h} ({face_area}px)"
            cv2.putText(frame, size_info, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            # In thông tin ra console
            print(f"👤 Khuôn mặt {i+1}: {age_estimate} | Kích thước: {w}x{h} | Diện tích: {face_area}")
        
        # Hiển thị số khuôn mặt
        info_text = f"Faces: {len(faces)} | SPACE: Analyze | ESC: Exit"
        cv2.putText(frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Hiển thị frame
        cv2.imshow('Quick Age Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            if len(faces) > 0:
                print(f"\n📊 PHÂN TÍCH CHI TIẾT:")
                print("=" * 30)
                for i, (x, y, w, h) in enumerate(faces):
                    face_area = w * h
                    age_estimate, _ = quick_age_estimate(w, h, face_area)
                    
                    print(f"👤 Khuôn mặt {i+1}:")
                    print(f"   🎂 Độ tuổi ước tính: {age_estimate}")
                    print(f"   📏 Kích thước: {w} x {h} pixels")
                    print(f"   📐 Diện tích: {face_area} pixels")
                    print(f"   📍 Vị trí: ({x}, {y})")
                    print()
            else:
                print("⚠️ Không phát hiện khuôn mặt!")
                print("💡 Hãy thử:")
                print("   - Di chuyển đến nơi có ánh sáng tốt hơn")
                print("   - Nhìn thẳng vào camera")
                print("   - Đến gần camera hơn")
                
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Đã thoát!")

if __name__ == "__main__":
    main()
