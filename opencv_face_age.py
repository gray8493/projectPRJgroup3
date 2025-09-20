import cv2
import numpy as np
import os
from datetime import datetime

class OpenCVFaceAgeDetector:
    def __init__(self):
        """Khởi tạo detector với OpenCV"""
        # Load Haar Cascade cho phát hiện khuôn mặt
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Các nhóm tuổi
        self.age_groups = {
            0: 'Trẻ em (0-12)',
            1: 'Thiếu niên (13-19)', 
            2: 'Thanh niên (20-35)',
            3: 'Trung niên (36-55)',
            4: 'Cao tuổi (56+)'
        }
        
        # Màu sắc cho các nhóm tuổi
        self.age_colors = {
            0: (255, 0, 255),    # Magenta - Trẻ em
            1: (0, 255, 255),    # Cyan - Thiếu niên
            2: (0, 255, 0),      # Green - Thanh niên
            3: (255, 255, 0),    # Yellow - Trung niên
            4: (0, 0, 255)       # Red - Cao tuổi
        }
    
    def detect_faces(self, frame):
        """Phát hiện khuôn mặt trong frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def analyze_face_features(self, face_region):
        """Phân tích đặc trưng khuôn mặt để ước tính tuổi"""
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        h, w = gray_face.shape
        
        # 1. Phân tích texture (độ nhám da)
        laplacian = cv2.Laplacian(gray_face, cv2.CV_64F)
        texture_variance = laplacian.var()
        
        # 2. Phân tích độ tương phản
        contrast = gray_face.std()
        
        # 3. Phân tích histogram
        hist = cv2.calcHist([gray_face], [0], None, [256], [0, 256])
        hist_mean = np.mean(hist)
        
        # 4. Phân tích cạnh (wrinkles)
        edges = cv2.Canny(gray_face, 50, 150)
        edge_density = np.sum(edges > 0) / (h * w)
        
        # 5. Phân tích kích thước tương đối
        face_area = h * w
        
        return {
            'texture_variance': texture_variance,
            'contrast': contrast,
            'hist_mean': hist_mean,
            'edge_density': edge_density,
            'face_area': face_area,
            'width': w,
            'height': h
        }
    
    def estimate_age_group(self, features):
        """Ước tính nhóm tuổi dựa trên đặc trưng"""
        score = 0
        
        # Texture analysis (da mịn = trẻ, da nhăn = già)
        if features['texture_variance'] > 500:
            score += 2  # Da mịn
        elif features['texture_variance'] > 200:
            score += 1
        else:
            score -= 1  # Da nhăn
        
        # Contrast analysis
        if features['contrast'] > 60:
            score += 1  # Tương phản cao = trẻ
        elif features['contrast'] < 30:
            score -= 1
        
        # Edge density (nhiều nếp nhăn = già)
        if features['edge_density'] < 0.1:
            score += 1  # Ít nếp nhăn
        elif features['edge_density'] > 0.2:
            score -= 1  # Nhiều nếp nhăn
        
        # Face size (khuôn mặt lớn thường là người lớn)
        if features['face_area'] < 5000:
            score += 2  # Khuôn mặt nhỏ = trẻ em
        elif features['face_area'] > 15000:
            score -= 1  # Khuôn mặt lớn = người lớn
        
        # Histogram analysis
        if features['hist_mean'] > 100:
            score += 1  # Da sáng = trẻ
        
        # Quyết định nhóm tuổi
        if score >= 4:
            return 0  # Trẻ em
        elif score >= 2:
            return 1  # Thiếu niên
        elif score >= 0:
            return 2  # Thanh niên
        elif score >= -2:
            return 3  # Trung niên
        else:
            return 4  # Cao tuổi
    
    def process_frame(self, frame):
        """Xử lý frame: phát hiện khuôn mặt và ước tính tuổi"""
        faces = self.detect_faces(frame)
        results = []
        
        for (x, y, w, h) in faces:
            # Cắt vùng khuôn mặt
            face_region = frame[y:y+h, x:x+w]
            
            # Phân tích đặc trưng
            features = self.analyze_face_features(face_region)
            
            # Ước tính nhóm tuổi
            age_group_id = self.estimate_age_group(features)
            age_group_name = self.age_groups[age_group_id]
            color = self.age_colors[age_group_id]
            
            # Vẽ bounding box với màu tương ứng
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Vẽ nhãn tuổi
            label = age_group_name
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # Vẽ background cho text
            cv2.rectangle(frame, (x, y-30), (x + label_size[0], y), color, -1)
            cv2.putText(frame, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Thêm thông tin chi tiết
            info_text = f"Texture: {features['texture_variance']:.0f}"
            cv2.putText(frame, info_text, (x, y+h+20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            results.append({
                'bbox': (x, y, w, h),
                'age_group': age_group_name,
                'age_id': age_group_id,
                'features': features
            })
        
        return frame, results

def main():
    print("🎯 Ứng dụng Nhận diện Khuôn mặt và Ước tính Độ tuổi")
    print("=" * 50)
    
    # Khởi tạo detector
    detector = OpenCVFaceAgeDetector()
    
    while True:
        print("\n📋 Chọn chế độ:")
        print("1. 📹 Camera trực tiếp")
        print("2. 📷 Phân tích ảnh")
        print("3. 📁 Phân tích thư mục ảnh")
        print("4. ❌ Thoát")
        
        choice = input("\n👉 Nhập lựa chọn (1-4): ").strip()
        
        if choice == '1':
            # Camera trực tiếp
            print("\n📹 Khởi động camera...")
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("❌ Không thể mở camera!")
                continue
            
            print("✅ Camera đã sẵn sàng!")
            print("💡 Nhấn 'q' để thoát, 's' để chụp ảnh")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Không thể đọc frame!")
                    break
                
                # Xử lý frame
                processed_frame, results = detector.process_frame(frame.copy())
                
                # Hiển thị thông tin
                info_text = f"Faces: {len(results)}"
                cv2.putText(processed_frame, info_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Hiển thị frame
                cv2.imshow('Face Age Detection', processed_frame)
                
                # Xử lý phím
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Lưu ảnh
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"capture_{timestamp}.jpg"
                    cv2.imwrite(filename, processed_frame)
                    print(f"📸 Đã lưu ảnh: {filename}")
            
            cap.release()
            cv2.destroyAllWindows()
        
        elif choice == '2':
            # Phân tích ảnh đơn lẻ
            image_path = input("\n📷 Nhập đường dẫn ảnh: ").strip()
            
            if not os.path.exists(image_path):
                print("❌ File không tồn tại!")
                continue
            
            # Đọc ảnh
            image = cv2.imread(image_path)
            if image is None:
                print("❌ Không thể đọc ảnh!")
                continue
            
            print("🔄 Đang phân tích...")
            
            # Xử lý ảnh
            processed_image, results = detector.process_frame(image.copy())
            
            # Hiển thị kết quả
            print(f"\n✅ Phát hiện {len(results)} khuôn mặt:")
            for i, result in enumerate(results):
                print(f"👤 Người {i+1}: {result['age_group']}")
                features = result['features']
                print(f"   - Texture: {features['texture_variance']:.0f}")
                print(f"   - Contrast: {features['contrast']:.1f}")
                print(f"   - Size: {features['width']}x{features['height']}")
            
            # Hiển thị ảnh
            cv2.imshow('Result', processed_image)
            print("\n💡 Nhấn phím bất kỳ để tiếp tục...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Lưu kết quả
            save = input("💾 Lưu kết quả? (y/n): ").strip().lower()
            if save == 'y':
                output_path = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(output_path, processed_image)
                print(f"✅ Đã lưu: {output_path}")
        
        elif choice == '3':
            # Phân tích thư mục
            folder_path = input("\n📁 Nhập đường dẫn thư mục: ").strip()
            
            if not os.path.exists(folder_path):
                print("❌ Thư mục không tồn tại!")
                continue
            
            # Tìm các file ảnh
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            image_files = []
            
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                print("❌ Không tìm thấy ảnh nào!")
                continue
            
            print(f"📊 Tìm thấy {len(image_files)} ảnh")
            
            # Tạo thư mục kết quả
            output_dir = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Xử lý từng ảnh
            total_faces = 0
            age_stats = {group: 0 for group in detector.age_groups.values()}
            
            for i, image_path in enumerate(image_files):
                print(f"🔄 Xử lý {i+1}/{len(image_files)}: {os.path.basename(image_path)}")
                
                image = cv2.imread(image_path)
                if image is None:
                    continue
                
                processed_image, results = detector.process_frame(image.copy())
                
                # Lưu kết quả
                output_path = os.path.join(output_dir, f"result_{os.path.basename(image_path)}")
                cv2.imwrite(output_path, processed_image)
                
                # Thống kê
                total_faces += len(results)
                for result in results:
                    age_stats[result['age_group']] += 1
            
            # Hiển thị thống kê
            print(f"\n📊 Thống kê tổng quan:")
            print(f"📷 Tổng số ảnh: {len(image_files)}")
            print(f"👥 Tổng số khuôn mặt: {total_faces}")
            print(f"📁 Kết quả lưu tại: {output_dir}")
            
            print(f"\n🎂 Phân bố độ tuổi:")
            for age_group, count in age_stats.items():
                if count > 0:
                    percentage = (count / total_faces) * 100 if total_faces > 0 else 0
                    print(f"   {age_group}: {count} người ({percentage:.1f}%)")
        
        elif choice == '4':
            print("👋 Tạm biệt!")
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
