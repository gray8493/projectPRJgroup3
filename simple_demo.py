#!/usr/bin/env python3
"""
Demo đơn giản chỉ sử dụng OpenCV để test
"""

def test_basic():
    """Test cơ bản không cần thư viện phức tạp"""
    print("🎯 Test Demo Đơn giản")
    print("=" * 40)
    
    try:
        import sys
        print(f"✅ Python version: {sys.version}")
    except Exception as e:
        print(f"❌ Python error: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
        print("💡 Hãy cài đặt: py -m pip install opencv-python")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
    except Exception as e:
        print(f"❌ NumPy error: {e}")
        print("💡 Hãy cài đặt: py -m pip install 'numpy<2.0'")
        return False
    
    # Test camera
    try:
        print("\n📹 Test camera...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera available")
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
        else:
            print("⚠️ Camera not available")
    except Exception as e:
        print(f"❌ Camera error: {e}")
    
    # Test face detection
    try:
        print("\n👤 Test face detection...")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if not face_cascade.empty():
            print("✅ Haar Cascade loaded successfully")
        else:
            print("❌ Failed to load Haar Cascade")
    except Exception as e:
        print(f"❌ Face detection error: {e}")
    
    print("\n🎉 Test hoàn thành!")
    return True

if __name__ == "__main__":
    test_basic()
    input("\nNhấn Enter để thoát...")
