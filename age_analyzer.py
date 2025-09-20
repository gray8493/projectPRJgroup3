#!/usr/bin/env python3
"""
Ứng dụng phân tích độ tuổi từ khuôn mặt
"""

import cv2
import numpy as np
import os
from datetime import datetime

class AgeAnalyzer:
    def __init__(self):
        """Khởi tạo bộ phân tích tuổi"""
        # Load face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Định nghĩa các nhóm tuổi
        self.age_groups = {
            0: 'Trẻ sơ sinh (0-2 tuổi)',
            1: 'Trẻ nhỏ (3-6 tuổi)', 
            2: 'Trẻ em (7-12 tuổi)',
            3: 'Thiếu niên (13-17 tuổi)',
            4: 'Thanh niên (18-25 tuổi)',
            5: 'Người trưởng thành (26-35 tuổi)',
            6: 'Trung niên (36-50 tuổi)',
            7: 'Cao tuổi (51-65 tuổi)',
            8: 'Người già (65+ tuổi)'
        }
        
        # Màu sắc cho từng nhóm tuổi
        self.age_colors = {
            0: (255, 192, 203),  # Pink - Trẻ sơ sinh
            1: (255, 165, 0),    # Orange - Trẻ nhỏ
            2: (255, 255, 0),    # Yellow - Trẻ em
            3: (0, 255, 255),    # Cyan - Thiếu niên
            4: (0, 255, 0),      # Green - Thanh niên
            5: (0, 128, 255),    # Blue - Trưởng thành
            6: (128, 0, 255),    # Purple - Trung niên
            7: (255, 0, 128),    # Magenta - Cao tuổi
            8: (128, 128, 128)   # Gray - Người già
        }
    
    def analyze_face_features(self, face_region):
        """Phân tích đặc trưng khuôn mặt để ước tính tuổi"""
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        h, w = gray_face.shape
        
        features = {}
        
        # 1. Phân tích kích thước khuôn mặt
        face_area = h * w
        features['face_area'] = face_area
        features['width'] = w
        features['height'] = h
        features['aspect_ratio'] = w / h if h > 0 else 1
        
        # 2. Phân tích texture (độ nhám da)
        laplacian = cv2.Laplacian(gray_face, cv2.CV_64F)
        features['texture_variance'] = laplacian.var()
        
        # 3. Phân tích độ tương phản
        features['contrast'] = gray_face.std()
        
        # 4. Phân tích histogram (phân bố độ sáng)
        hist = cv2.calcHist([gray_face], [0], None, [256], [0, 256])
        features['hist_mean'] = np.mean(hist)
        features['hist_std'] = np.std(hist)
        
        # 5. Phân tích cạnh (nếp nhăn)
        edges = cv2.Canny(gray_face, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / (h * w)
        
        # 6. Phân tích gradient (độ thay đổi cường độ)
        grad_x = cv2.Sobel(gray_face, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray_face, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        features['gradient_mean'] = np.mean(gradient_magnitude)
        
        # 7. Phân tích độ mịn da
        blur = cv2.GaussianBlur(gray_face, (5, 5), 0)
        features['smoothness'] = np.mean(np.abs(gray_face.astype(float) - blur.astype(float)))
        
        return features
    
    def estimate_age_group(self, features):
        """Ước tính nhóm tuổi dựa trên đặc trưng"""
        score = 0
        confidence = 0
        
        # Phân tích kích thước khuôn mặt
        face_area = features['face_area']
        if face_area < 3000:
            score += 3  # Rất nhỏ - trẻ sơ sinh/trẻ nhỏ
            confidence += 0.8
        elif face_area < 6000:
            score += 2  # Nhỏ - trẻ em
            confidence += 0.7
        elif face_area < 12000:
            score += 1  # Trung bình - thiếu niên/thanh niên
            confidence += 0.6
        elif face_area > 20000:
            score -= 1  # Lớn - người lớn
            confidence += 0.5
        
        # Phân tích texture (da mịn = trẻ, da nhăn = già)
        texture = features['texture_variance']
        if texture > 800:
            score += 2  # Da rất mịn
            confidence += 0.7
        elif texture > 400:
            score += 1  # Da mịn
            confidence += 0.6
        elif texture < 100:
            score -= 2  # Da nhăn nhiều
            confidence += 0.8
        elif texture < 200:
            score -= 1  # Da có nếp nhăn
            confidence += 0.6
        
        # Phân tích độ tương phản
        contrast = features['contrast']
        if contrast > 60:
            score += 1  # Tương phản cao = da trẻ
            confidence += 0.5
        elif contrast < 30:
            score -= 1  # Tương phản thấp = da già
            confidence += 0.5
        
        # Phân tích mật độ cạnh (nếp nhăn)
        edge_density = features['edge_density']
        if edge_density < 0.05:
            score += 2  # Ít nếp nhăn = trẻ
            confidence += 0.7
        elif edge_density < 0.1:
            score += 1
            confidence += 0.5
        elif edge_density > 0.2:
            score -= 2  # Nhiều nếp nhăn = già
            confidence += 0.8
        elif edge_density > 0.15:
            score -= 1
            confidence += 0.6
        
        # Phân tích độ mịn da
        smoothness = features['smoothness']
        if smoothness < 5:
            score += 2  # Da rất mịn
            confidence += 0.6
        elif smoothness < 10:
            score += 1  # Da mịn
            confidence += 0.4
        elif smoothness > 20:
            score -= 1  # Da không mịn
            confidence += 0.4
        
        # Phân tích gradient
        gradient = features['gradient_mean']
        if gradient < 15:
            score += 1  # Gradient thấp = da mịn
            confidence += 0.3
        elif gradient > 30:
            score -= 1  # Gradient cao = da nhăn
            confidence += 0.3
        
        # Tính confidence trung bình
        confidence = min(confidence / 6, 1.0)
        
        # Quyết định nhóm tuổi dựa trên score
        if score >= 8:
            return 0, confidence  # Trẻ sơ sinh
        elif score >= 6:
            return 1, confidence  # Trẻ nhỏ
        elif score >= 4:
            return 2, confidence  # Trẻ em
        elif score >= 2:
            return 3, confidence  # Thiếu niên
        elif score >= 0:
            return 4, confidence  # Thanh niên
        elif score >= -2:
            return 5, confidence  # Trưởng thành
        elif score >= -4:
            return 6, confidence  # Trung niên
        elif score >= -6:
            return 7, confidence  # Cao tuổi
        else:
            return 8, confidence  # Người già
    
    def analyze_image(self, image_path):
        """Phân tích ảnh và ước tính tuổi"""
        # Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Không thể đọc ảnh!")
            return None
        
        # Phát hiện khuôn mặt
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            print("⚠️ Không phát hiện khuôn mặt nào!")
            return None
        
        results = []
        result_image = image.copy()
        
        print(f"\n🔍 Phân tích {len(faces)} khuôn mặt:")
        print("=" * 50)
        
        for i, (x, y, w, h) in enumerate(faces):
            print(f"\n👤 Khuôn mặt {i+1}:")
            
            # Cắt vùng khuôn mặt
            face_region = image[y:y+h, x:x+w]
            
            # Phân tích đặc trưng
            features = self.analyze_face_features(face_region)
            
            # Ước tính tuổi
            age_group_id, confidence = self.estimate_age_group(features)
            age_group_name = self.age_groups[age_group_id]
            color = self.age_colors[age_group_id]
            
            # In thông tin chi tiết
            print(f"   🎂 Độ tuổi ước tính: {age_group_name}")
            print(f"   📊 Độ tin cậy: {confidence:.1%}")
            print(f"   📏 Kích thước: {w}x{h} pixels")
            print(f"   📐 Diện tích: {features['face_area']} pixels")
            print(f"   🎨 Texture: {features['texture_variance']:.1f}")
            print(f"   🌟 Contrast: {features['contrast']:.1f}")
            print(f"   📈 Edge density: {features['edge_density']:.3f}")
            print(f"   ✨ Smoothness: {features['smoothness']:.1f}")
            
            # Vẽ kết quả lên ảnh
            cv2.rectangle(result_image, (x, y), (x+w, y+h), color, 2)
            
            # Vẽ nhãn tuổi
            label = f"{age_group_name}"
            confidence_text = f"({confidence:.0%})"
            
            # Tính kích thước text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            
            (label_w, label_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
            (conf_w, conf_h), _ = cv2.getTextSize(confidence_text, font, font_scale, thickness)
            
            # Vẽ background cho text
            cv2.rectangle(result_image, (x, y-35), (x + max(label_w, conf_w) + 10, y), color, -1)
            
            # Vẽ text
            cv2.putText(result_image, label, (x+5, y-20), font, font_scale, (255, 255, 255), thickness)
            cv2.putText(result_image, confidence_text, (x+5, y-5), font, font_scale, (255, 255, 255), thickness)
            
            # Lưu thông tin
            results.append({
                'id': i+1,
                'bbox': (x, y, w, h),
                'age_group': age_group_name,
                'age_id': age_group_id,
                'confidence': confidence,
                'features': features
            })
        
        return result_image, results
    
    def capture_and_analyze(self):
        """Chụp ảnh từ camera và phân tích"""
        print("📸 Chụp ảnh và Phân tích Tuổi")
        print("=" * 40)
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Không thể mở camera!")
            return
        
        print("✅ Camera đã sẵn sàng!")
        print("💡 Nhấn SPACE để chụp ảnh, ESC để thoát")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Phát hiện khuôn mặt real-time
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
            
            # Vẽ khung khuôn mặt
            display_frame = frame.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(display_frame, 'Face Ready', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Hiển thị hướng dẫn
            cv2.putText(display_frame, f"Faces: {len(faces)} | SPACE: Capture | ESC: Exit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Age Analysis - Capture', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 32:  # SPACE
                # Chụp ảnh
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"age_photo_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                
                print(f"\n📸 Đã chụp ảnh: {filename}")
                
                # Phân tích ảnh
                result_image, results = self.analyze_image(filename)
                
                if results:
                    # Lưu ảnh kết quả
                    result_filename = f"age_result_{timestamp}.jpg"
                    cv2.imwrite(result_filename, result_image)
                    print(f"💾 Đã lưu kết quả: {result_filename}")
                    
                    # Hiển thị kết quả
                    cv2.imshow('Age Analysis Result', result_image)
                    print("\n👁️ Nhấn phím bất kỳ để tiếp tục...")
                    cv2.waitKey(0)
                    cv2.destroyWindow('Age Analysis Result')
                
                # Hỏi có muốn chụp tiếp
                choice = input("\n📷 Chụp ảnh khác? (y/n): ").strip().lower()
                if choice != 'y':
                    break
                    
            elif key == 27:  # ESC
                break
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    print("🎯 Phân tích Độ tuổi từ Khuôn mặt")
    print("=" * 50)
    
    analyzer = AgeAnalyzer()
    
    while True:
        print("\n📋 Chọn chế độ:")
        print("1. 📸 Chụp ảnh và phân tích tuổi")
        print("2. 📁 Phân tích ảnh có sẵn")
        print("3. 📊 Phân tích hàng loạt")
        print("4. ❌ Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (1-4): ").strip()
        
        if choice == '1':
            analyzer.capture_and_analyze()
            
        elif choice == '2':
            # Liệt kê ảnh có sẵn
            image_files = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
            if image_files:
                print("\n📷 Ảnh có sẵn:")
                for i, file in enumerate(image_files):
                    print(f"   {i+1}. {file}")
                
                try:
                    idx = int(input(f"\nChọn ảnh (1-{len(image_files)}): ")) - 1
                    if 0 <= idx < len(image_files):
                        filename = image_files[idx]
                        result_image, results = analyzer.analyze_image(filename)
                        
                        if results:
                            # Hiển thị kết quả
                            cv2.imshow('Age Analysis Result', result_image)
                            print("\n👁️ Nhấn phím bất kỳ để đóng...")
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            
                            # Lưu kết quả
                            save = input("\n💾 Lưu kết quả? (y/n): ").strip().lower()
                            if save == 'y':
                                result_filename = f"age_analyzed_{datetime.now().strftime('%H%M%S')}.jpg"
                                cv2.imwrite(result_filename, result_image)
                                print(f"✅ Đã lưu: {result_filename}")
                    else:
                        print("❌ Lựa chọn không hợp lệ!")
                except ValueError:
                    print("❌ Vui lòng nhập số!")
            else:
                filename = input("📷 Nhập đường dẫn ảnh: ").strip()
                if os.path.exists(filename):
                    analyzer.analyze_image(filename)
                else:
                    print("❌ File không tồn tại!")
        
        elif choice == '3':
            print("📊 Tính năng phân tích hàng loạt sẽ được bổ sung...")
            
        elif choice == '4':
            print("👋 Tạm biệt!")
            break
            
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
