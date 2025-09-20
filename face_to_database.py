#!/usr/bin/env python3
"""
Ứng dụng quét khuôn mặt và lưu dữ liệu vào MySQL database
"""

import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import json
import hashlib

class FaceDatabaseSystem:
    def __init__(self):
        """Khởi tạo hệ thống quét khuôn mặt và database"""
        # Load face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Database connection
        self.db_connection = None
        self.cursor = None
        
        # Định nghĩa các nhóm tuổi
        self.age_groups = {
            0: 'Trẻ em (0-12)',
            1: 'Thiếu niên (13-17)', 
            2: 'Thanh niên (18-25)',
            3: 'Trưởng thành (26-35)',
            4: 'Trung niên (36-50)',
            5: 'Cao tuổi (50+)'
        }
    
    def connect_database(self, host='localhost', user='root', password='', database='face_recognition'):
        """Kết nối đến MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.db_connection.cursor()
            print("✅ Đã kết nối database thành công!")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Lỗi kết nối database: {err}")
            return False
    
    def create_database_tables(self):
        """Tạo bảng trong database nếu chưa có"""
        try:
            # Tạo bảng face_scans
            create_table_query = """
            CREATE TABLE IF NOT EXISTS face_scans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scan_time DATETIME NOT NULL,
                face_count INT NOT NULL,
                session_id VARCHAR(50) NOT NULL,
                location VARCHAR(100),
                notes TEXT
            )
            """
            self.cursor.execute(create_table_query)
            
            # Tạo bảng face_data
            create_face_data_query = """
            CREATE TABLE IF NOT EXISTS face_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scan_id INT,
                face_number INT NOT NULL,
                age_group VARCHAR(50) NOT NULL,
                age_confidence FLOAT,
                face_width INT NOT NULL,
                face_height INT NOT NULL,
                face_area INT NOT NULL,
                position_x INT NOT NULL,
                position_y INT NOT NULL,
                texture_variance FLOAT,
                contrast_level FLOAT,
                edge_density FLOAT,
                smoothness FLOAT,
                face_hash VARCHAR(64),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scan_id) REFERENCES face_scans(id)
            )
            """
            self.cursor.execute(create_face_data_query)
            
            self.db_connection.commit()
            print("✅ Đã tạo bảng database thành công!")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Lỗi tạo bảng: {err}")
            return False
    
    def analyze_face_features(self, face_region):
        """Phân tích đặc trưng khuôn mặt"""
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        h, w = gray_face.shape
        
        features = {}
        
        # Kích thước và diện tích
        features['width'] = w
        features['height'] = h
        features['area'] = w * h
        
        # Phân tích texture
        laplacian = cv2.Laplacian(gray_face, cv2.CV_64F)
        features['texture_variance'] = float(laplacian.var())
        
        # Độ tương phản
        features['contrast'] = float(gray_face.std())
        
        # Mật độ cạnh
        edges = cv2.Canny(gray_face, 50, 150)
        features['edge_density'] = float(np.sum(edges > 0) / (h * w))
        
        # Độ mịn
        blur = cv2.GaussianBlur(gray_face, (5, 5), 0)
        features['smoothness'] = float(np.mean(np.abs(gray_face.astype(float) - blur.astype(float))))
        
        return features
    
    def estimate_age_group(self, features):
        """Ước tính nhóm tuổi"""
        score = 0
        confidence = 0
        
        # Phân tích kích thước
        face_area = features['area']
        if face_area < 5000:
            score += 2
            confidence += 0.7
        elif face_area < 10000:
            score += 1
            confidence += 0.6
        elif face_area > 20000:
            score -= 1
            confidence += 0.5
        
        # Phân tích texture
        texture = features['texture_variance']
        if texture > 500:
            score += 2
            confidence += 0.8
        elif texture > 200:
            score += 1
            confidence += 0.6
        elif texture < 100:
            score -= 2
            confidence += 0.8
        
        # Phân tích contrast
        contrast = features['contrast']
        if contrast > 50:
            score += 1
            confidence += 0.5
        elif contrast < 30:
            score -= 1
            confidence += 0.5
        
        # Phân tích edge density
        edge_density = features['edge_density']
        if edge_density < 0.1:
            score += 1
            confidence += 0.6
        elif edge_density > 0.2:
            score -= 1
            confidence += 0.6
        
        # Tính confidence trung bình
        confidence = min(confidence / 4, 1.0)
        
        # Quyết định nhóm tuổi
        if score >= 4:
            return 0, confidence  # Trẻ em
        elif score >= 2:
            return 1, confidence  # Thiếu niên
        elif score >= 0:
            return 2, confidence  # Thanh niên
        elif score >= -1:
            return 3, confidence  # Trưởng thành
        elif score >= -2:
            return 4, confidence  # Trung niên
        else:
            return 5, confidence  # Cao tuổi
    
    def generate_face_hash(self, face_region):
        """Tạo hash cho khuôn mặt để tránh trùng lặp"""
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        # Resize về kích thước chuẩn
        resized = cv2.resize(gray_face, (64, 64))
        # Tạo hash
        face_bytes = resized.tobytes()
        return hashlib.sha256(face_bytes).hexdigest()
    
    def save_scan_to_database(self, faces_data, location="", notes=""):
        """Lưu dữ liệu quét vào database"""
        try:
            # Tạo session ID
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Lưu thông tin scan chính
            scan_query = """
            INSERT INTO face_scans (scan_time, face_count, session_id, location, notes)
            VALUES (%s, %s, %s, %s, %s)
            """
            scan_data = (
                datetime.now(),
                len(faces_data),
                session_id,
                location,
                notes
            )
            
            self.cursor.execute(scan_query, scan_data)
            scan_id = self.cursor.lastrowid
            
            # Lưu dữ liệu từng khuôn mặt
            face_query = """
            INSERT INTO face_data (
                scan_id, face_number, age_group, age_confidence,
                face_width, face_height, face_area,
                position_x, position_y,
                texture_variance, contrast_level, edge_density, smoothness,
                face_hash
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for i, face_data in enumerate(faces_data):
                face_values = (
                    scan_id,
                    i + 1,
                    face_data['age_group'],
                    float(face_data['confidence']),
                    int(face_data['features']['width']),
                    int(face_data['features']['height']),
                    int(face_data['features']['area']),
                    int(face_data['position'][0]),
                    int(face_data['position'][1]),
                    float(face_data['features']['texture_variance']),
                    float(face_data['features']['contrast']),
                    float(face_data['features']['edge_density']),
                    float(face_data['features']['smoothness']),
                    face_data['face_hash']
                )
                
                self.cursor.execute(face_query, face_values)
            
            self.db_connection.commit()
            
            print(f"✅ Đã lưu {len(faces_data)} khuôn mặt vào database!")
            print(f"📊 Session ID: {session_id}")
            print(f"🆔 Scan ID: {scan_id}")
            
            return scan_id, session_id
            
        except mysql.connector.Error as err:
            print(f"❌ Lỗi lưu database: {err}")
            return None, None
    
    def scan_faces_live(self):
        """Quét khuôn mặt trực tiếp từ camera"""
        print("📹 Khởi động camera để quét khuôn mặt...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Không thể mở camera!")
            return
        
        print("✅ Camera đã sẵn sàng!")
        print("💡 Nhấn SPACE để quét và lưu vào database, ESC để thoát")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Phát hiện khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
            
            # Vẽ khung khuôn mặt và thông tin
            display_frame = frame.copy()
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(display_frame, f'Face {i+1}', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Hiển thị thông tin
            info_text = f"Faces: {len(faces)} | SPACE: Save to DB | ESC: Exit"
            cv2.putText(display_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Face Scanner - Database Mode', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 32:  # SPACE
                if len(faces) > 0:
                    print(f"\n🔍 Đang phân tích {len(faces)} khuôn mặt...")
                    
                    faces_data = []
                    
                    for i, (x, y, w, h) in enumerate(faces):
                        # Cắt vùng khuôn mặt
                        face_region = frame[y:y+h, x:x+w]
                        
                        # Phân tích đặc trưng
                        features = self.analyze_face_features(face_region)
                        
                        # Ước tính tuổi
                        age_group_id, confidence = self.estimate_age_group(features)
                        age_group_name = self.age_groups[age_group_id]
                        
                        # Tạo hash
                        face_hash = self.generate_face_hash(face_region)
                        
                        # Lưu dữ liệu
                        face_data = {
                            'position': (x, y),
                            'age_group': age_group_name,
                            'confidence': confidence,
                            'features': features,
                            'face_hash': face_hash
                        }
                        
                        faces_data.append(face_data)
                        
                        print(f"👤 Khuôn mặt {i+1}: {age_group_name} ({confidence:.1%})")
                    
                    # Nhập thông tin bổ sung
                    location = input("📍 Nhập vị trí (tùy chọn): ").strip()
                    notes = input("📝 Nhập ghi chú (tùy chọn): ").strip()
                    
                    # Lưu vào database
                    scan_id, session_id = self.save_scan_to_database(faces_data, location, notes)
                    
                    if scan_id:
                        print("🎉 Đã lưu thành công!")
                    
                else:
                    print("⚠️ Không phát hiện khuôn mặt nào!")
                    
            elif key == 27:  # ESC
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def view_database_stats(self):
        """Xem thống kê database"""
        try:
            # Thống kê tổng quan
            self.cursor.execute("SELECT COUNT(*) FROM face_scans")
            total_scans = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM face_data")
            total_faces = self.cursor.fetchone()[0]
            
            print(f"\n📊 THỐNG KÊ DATABASE:")
            print("=" * 30)
            print(f"🔍 Tổng số lần quét: {total_scans}")
            print(f"👥 Tổng số khuôn mặt: {total_faces}")
            
            # Thống kê theo nhóm tuổi
            self.cursor.execute("""
                SELECT age_group, COUNT(*) as count 
                FROM face_data 
                GROUP BY age_group 
                ORDER BY count DESC
            """)
            
            age_stats = self.cursor.fetchall()
            
            print(f"\n🎂 PHÂN BỐ THEO TUỔI:")
            for age_group, count in age_stats:
                percentage = (count / total_faces) * 100 if total_faces > 0 else 0
                print(f"   {age_group}: {count} người ({percentage:.1f}%)")
            
            # Lần quét gần nhất
            self.cursor.execute("""
                SELECT scan_time, face_count, location 
                FROM face_scans 
                ORDER BY scan_time DESC 
                LIMIT 5
            """)
            
            recent_scans = self.cursor.fetchall()
            
            print(f"\n⏰ 5 LẦN QUÉT GẦN NHẤT:")
            for scan_time, face_count, location in recent_scans:
                loc_text = f" tại {location}" if location else ""
                print(f"   {scan_time}: {face_count} khuôn mặt{loc_text}")
                
        except mysql.connector.Error as err:
            print(f"❌ Lỗi truy vấn database: {err}")
    
    def close_connection(self):
        """Đóng kết nối database"""
        if self.cursor:
            self.cursor.close()
        if self.db_connection:
            self.db_connection.close()
        print("✅ Đã đóng kết nối database")

def setup_database():
    """Hướng dẫn thiết lập database"""
    print("🗄️ THIẾT LẬP DATABASE MYSQL")
    print("=" * 40)
    print("1. Cài đặt MySQL Server")
    print("2. Tạo database 'face_recognition'")
    print("3. Cài đặt mysql-connector-python:")
    print("   py -m pip install mysql-connector-python")
    print()
    
    host = input("🌐 MySQL Host (localhost): ").strip() or "localhost"
    user = input("👤 MySQL User (root): ").strip() or "root"
    password = input("🔐 MySQL Password: ").strip()
    database = input("🗄️ Database name (face_recognition): ").strip() or "face_recognition"
    
    return host, user, password, database

def main():
    print("🎯 Hệ thống Quét Khuôn mặt - Database MySQL")
    print("=" * 50)
    
    # Thiết lập database
    host, user, password, database = setup_database()
    
    # Khởi tạo hệ thống
    system = FaceDatabaseSystem()
    
    # Kết nối database
    if not system.connect_database(host, user, password, database):
        print("❌ Không thể kết nối database!")
        return
    
    # Tạo bảng
    if not system.create_database_tables():
        print("❌ Không thể tạo bảng!")
        return
    
    try:
        while True:
            print("\n📋 MENU CHÍNH:")
            print("1. 📹 Quét khuôn mặt trực tiếp")
            print("2. 📊 Xem thống kê database")
            print("3. ❌ Thoát")
            
            choice = input("\n👉 Chọn (1-3): ").strip()
            
            if choice == '1':
                system.scan_faces_live()
            elif choice == '2':
                system.view_database_stats()
            elif choice == '3':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
    finally:
        system.close_connection()
        print("👋 Tạm biệt!")

if __name__ == "__main__":
    main()
