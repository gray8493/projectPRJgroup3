import cv2
import numpy as np
import streamlit as st
from PIL import Image
import os

class SimpleFaceAgeDetector:
    def __init__(self):
        """Khởi tạo detector đơn giản với Haar Cascades"""
        # Sử dụng Haar Cascade có sẵn trong OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Các nhóm tuổi để phân loại
        self.age_groups = ['Trẻ em (0-12)', 'Thiếu niên (13-19)', 'Thanh niên (20-35)', 
                          'Trung niên (36-55)', 'Cao tuổi (56+)']
    
    def detect_faces(self, image):
        """Phát hiện khuôn mặt sử dụng Haar Cascades"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        return faces
    
    def estimate_age_simple(self, face_region):
        """Ước tính độ tuổi đơn giản dựa trên đặc trưng khuôn mặt"""
        # Chuyển sang grayscale
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        
        # Tính toán một số đặc trưng đơn giản
        height, width = gray_face.shape
        
        # Phân tích texture (độ nhám của da)
        laplacian_var = cv2.Laplacian(gray_face, cv2.CV_64F).var()
        
        # Phân tích độ tương phản
        contrast = gray_face.std()
        
        # Phân tích histogram
        hist = cv2.calcHist([gray_face], [0], None, [256], [0, 256])
        hist_mean = np.mean(hist)
        
        # Logic đơn giản để ước tính tuổi
        age_score = 0
        
        # Texture score (da nhăn nhiều = tuổi cao)
        if laplacian_var < 100:
            age_score += 2  # Da mịn = trẻ
        elif laplacian_var < 300:
            age_score += 1
        else:
            age_score += 0  # Da nhăn = già
        
        # Contrast score
        if contrast > 50:
            age_score += 1  # Tương phản cao = trẻ
        
        # Size score (khuôn mặt lớn thường là người lớn)
        face_area = height * width
        if face_area > 10000:
            age_score -= 1
        
        # Quyết định nhóm tuổi
        if age_score >= 3:
            return self.age_groups[0]  # Trẻ em
        elif age_score >= 2:
            return self.age_groups[1]  # Thiếu niên
        elif age_score >= 1:
            return self.age_groups[2]  # Thanh niên
        elif age_score >= 0:
            return self.age_groups[3]  # Trung niên
        else:
            return self.age_groups[4]  # Cao tuổi
    
    def process_image(self, image):
        """Xử lý ảnh: phát hiện khuôn mặt và ước tính độ tuổi"""
        faces = self.detect_faces(image)
        results = []
        
        for (x, y, w, h) in faces:
            # Cắt vùng khuôn mặt
            face_region = image[y:y+h, x:x+w]
            
            # Ước tính tuổi
            estimated_age = self.estimate_age_simple(face_region)
            
            # Vẽ bounding box
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Vẽ text tuổi
            cv2.putText(image, estimated_age, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            results.append({
                'bbox': (x, y, w, h),
                'age': estimated_age
            })
        
        return image, results

def main():
    st.set_page_config(
        page_title="Ứng dụng Nhận diện Tuổi Đơn giản",
        page_icon="👤",
        layout="wide"
    )
    
    st.title("🎯 Ứng dụng Nhận diện Khuôn mặt và Ước tính Độ tuổi")
    st.markdown("*Phiên bản đơn giản sử dụng OpenCV Haar Cascades*")
    st.markdown("---")
    
    # Khởi tạo detector
    detector = SimpleFaceAgeDetector()
    
    # Sidebar
    st.sidebar.title("⚙️ Cài đặt")
    st.sidebar.markdown("### 📋 Hướng dẫn sử dụng:")
    st.sidebar.markdown("""
    1. **Camera trực tiếp**: Sử dụng webcam để phân tích real-time
    2. **Tải ảnh lên**: Upload ảnh từ máy tính
    3. **Chụp ảnh**: Chụp ảnh trực tiếp từ camera
    """)
    
    # Chọn chế độ
    mode = st.sidebar.selectbox(
        "📷 Chọn chế độ:",
        ["Tải ảnh lên", "Camera trực tiếp", "Chụp ảnh"]
    )
    
    if mode == "Tải ảnh lên":
        st.subheader("📤 Tải ảnh lên để phân tích")
        
        uploaded_file = st.file_uploader(
            "Chọn ảnh:",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Hỗ trợ: JPG, JPEG, PNG, BMP"
        )
        
        if uploaded_file is not None:
            # Đọc và hiển thị ảnh
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # Chuyển đổi RGB sang BGR
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            else:
                image_cv = image_np
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📷 Ảnh gốc")
                st.image(image, use_column_width=True)
            
            # Xử lý ảnh
            with st.spinner("🔄 Đang phân tích khuôn mặt..."):
                processed_image, results = detector.process_image(image_cv.copy())
                processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.subheader("🎯 Kết quả phân tích")
                st.image(processed_image_rgb, use_column_width=True)
            
            # Hiển thị kết quả
            st.markdown("---")
            if results:
                st.success(f"✅ Phát hiện **{len(results)}** khuôn mặt!")
                
                # Tạo bảng kết quả
                for i, result in enumerate(results):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        st.metric("👤 Người", f"#{i+1}")
                    
                    with col2:
                        st.metric("🎂 Độ tuổi ước tính", result['age'])
                    
                    with col3:
                        x, y, w, h = result['bbox']
                        st.metric("📏 Kích thước", f"{w}x{h}")
                
                # Thống kê
                st.markdown("### 📊 Thống kê")
                age_counts = {}
                for result in results:
                    age = result['age']
                    age_counts[age] = age_counts.get(age, 0) + 1
                
                for age_group, count in age_counts.items():
                    st.write(f"- **{age_group}**: {count} người")
                    
            else:
                st.warning("⚠️ Không phát hiện khuôn mặt nào trong ảnh!")
                st.info("💡 **Gợi ý**: Hãy thử với ảnh có khuôn mặt rõ ràng hơn")
    
    elif mode == "Camera trực tiếp":
        st.subheader("📹 Camera trực tiếp")
        
        # Kiểm tra camera
        if st.button("🔍 Kiểm tra Camera"):
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                st.success("✅ Camera hoạt động bình thường!")
                cap.release()
            else:
                st.error("❌ Không thể truy cập camera!")
        
        st.info("💡 **Lưu ý**: Tính năng camera trực tiếp cần chạy ứng dụng local để hoạt động tốt nhất")
        
        # Hướng dẫn chạy local
        st.markdown("### 🚀 Để sử dụng camera trực tiếp:")
        st.code("streamlit run simple_face_age_app.py", language="bash")
    
    else:  # Chụp ảnh
        st.subheader("📸 Chụp ảnh")
        
        # Sử dụng camera component của Streamlit
        picture = st.camera_input("Chụp ảnh để phân tích:")
        
        if picture is not None:
            # Xử lý ảnh được chụp
            image = Image.open(picture)
            image_np = np.array(image)
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📷 Ảnh vừa chụp")
                st.image(image, use_column_width=True)
            
            with st.spinner("🔄 Đang phân tích..."):
                processed_image, results = detector.process_image(image_cv.copy())
                processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.subheader("🎯 Kết quả phân tích")
                st.image(processed_image_rgb, use_column_width=True)
            
            # Hiển thị kết quả
            if results:
                st.success(f"✅ Phát hiện {len(results)} khuôn mặt!")
                for i, result in enumerate(results):
                    st.info(f"👤 **Người {i+1}:** {result['age']}")
            else:
                st.warning("⚠️ Không phát hiện khuôn mặt!")
    
    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ Thông tin")
    st.markdown("""
    - **Công nghệ**: OpenCV Haar Cascades
    - **Độ chính xác**: Ước tính cơ bản
    - **Hỗ trợ**: Phát hiện nhiều khuôn mặt
    - **Tác giả**: AI Assistant
    """)

if __name__ == "__main__":
    main()
