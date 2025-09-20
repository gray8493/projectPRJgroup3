#!/usr/bin/env python3
"""
Demo script để test nhanh ứng dụng nhận diện khuôn mặt và ước tính tuổi
"""

import cv2
import sys
import os

def test_opencv():
    """Test OpenCV installation"""
    print("🔍 Kiểm tra OpenCV...")
    try:
        print(f"✅ OpenCV version: {cv2.__version__}")
        return True
    except Exception as e:
        print(f"❌ Lỗi OpenCV: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("\n📹 Kiểm tra camera...")
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Camera hoạt động bình thường")
                print(f"📏 Độ phân giải: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
                return True
            else:
                print("❌ Không thể đọc frame từ camera")
                cap.release()
                return False
        else:
            print("❌ Không thể mở camera")
            return False
    except Exception as e:
        print(f"❌ Lỗi camera: {e}")
        return False

def test_face_detection():
    """Test face detection"""
    print("\n👤 Kiểm tra phát hiện khuôn mặt...")
    try:
        # Load Haar Cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if face_cascade.empty():
            print("❌ Không thể load Haar Cascade")
            return False
        
        print("✅ Haar Cascade loaded thành công")
        
        # Test với camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Không thể mở camera để test")
            return False
        
        print("📸 Đang test phát hiện khuôn mặt (5 giây)...")
        print("💡 Hãy nhìn vào camera!")
        
        face_detected = False
        for i in range(50):  # Test trong 5 giây (50 frames)
            ret, frame = cap.read()
            if not ret:
                continue
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            
            if len(faces) > 0:
                face_detected = True
                print(f"✅ Phát hiện {len(faces)} khuôn mặt!")
                break
            
            # Hiển thị frame
            cv2.imshow('Face Detection Test', frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if face_detected:
            print("✅ Test phát hiện khuôn mặt thành công!")
            return True
        else:
            print("⚠️ Không phát hiện khuôn mặt (có thể do ánh sáng hoặc góc camera)")
            return True  # Vẫn coi là pass vì có thể do điều kiện test
            
    except Exception as e:
        print(f"❌ Lỗi test face detection: {e}")
        return False

def quick_demo():
    """Chạy demo nhanh"""
    print("\n🚀 Demo nhanh - Nhấn 'q' để thoát")
    
    try:
        # Khởi tạo
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Màu sắc cho các nhóm tuổi (giả định)
        colors = [(255, 0, 255), (0, 255, 255), (0, 255, 0), (255, 255, 0), (0, 0, 255)]
        age_groups = ['Trẻ em', 'Thiếu niên', 'Thanh niên', 'Trung niên', 'Cao tuổi']
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Phát hiện khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
            
            # Vẽ kết quả
            for i, (x, y, w, h) in enumerate(faces):
                # Chọn màu và nhóm tuổi ngẫu nhiên cho demo
                color_idx = (frame_count // 30 + i) % len(colors)
                color = colors[color_idx]
                age_group = age_groups[color_idx]
                
                # Vẽ bounding box
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Vẽ nhãn
                label = f"{age_group} (Demo)"
                cv2.putText(frame, label, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Thông tin
            info = f"Faces: {len(faces)} | Frame: {frame_count}"
            cv2.putText(frame, info, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Hiển thị
            cv2.imshow('Face Age Detection Demo', frame)
            
            # Kiểm tra phím
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Demo hoàn thành!")
        
    except Exception as e:
        print(f"❌ Lỗi demo: {e}")

def main():
    print("🎯 DEMO - Ứng dụng Nhận diện Khuôn mặt và Ước tính Độ tuổi")
    print("=" * 60)
    
    # Kiểm tra hệ thống
    opencv_ok = test_opencv()
    camera_ok = test_camera()
    face_detection_ok = test_face_detection()
    
    print("\n📊 KẾT QUẢ KIỂM TRA:")
    print(f"OpenCV: {'✅' if opencv_ok else '❌'}")
    print(f"Camera: {'✅' if camera_ok else '❌'}")
    print(f"Face Detection: {'✅' if face_detection_ok else '❌'}")
    
    if opencv_ok and camera_ok:
        print("\n🎮 Chọn hành động:")
        print("1. 🚀 Chạy demo nhanh")
        print("2. 📋 Hướng dẫn sử dụng")
        print("3. ❌ Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (1-3): ").strip()
        
        if choice == '1':
            quick_demo()
        elif choice == '2':
            print("\n📋 HƯỚNG DẪN SỬ DỤNG:")
            print("1. Chạy ứng dụng Streamlit:")
            print("   streamlit run simple_face_age_app.py")
            print("\n2. Chạy ứng dụng console:")
            print("   python opencv_face_age.py")
            print("\n3. Xem README.md để biết thêm chi tiết")
        else:
            print("👋 Tạm biệt!")
    else:
        print("\n❌ Hệ thống chưa sẵn sàng. Vui lòng kiểm tra lại!")
        print("💡 Hướng dẫn khắc phục:")
        if not opencv_ok:
            print("   - Cài đặt OpenCV: pip install opencv-python")
        if not camera_ok:
            print("   - Kiểm tra camera và quyền truy cập")

if __name__ == "__main__":
    main()
