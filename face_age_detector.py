import cv2
import numpy as np
import streamlit as st
from PIL import Image
import tempfile
import os

class FaceAgeDetector:
    def __init__(self):
        """Khởi tạo detector với các model pre-trained"""
        # Tải model phát hiện khuôn mặt
        self.face_net = cv2.dnn.readNetFromTensorflow('models/opencv_face_detector_uint8.pb', 
                                                      'models/opencv_face_detector.pbtxt')
        
        # Tải model ước tính độ tuổi
        self.age_net = cv2.dnn.readNetFromCaffe('models/age_deploy.prototxt', 
                                                'models/age_net.caffemodel')
        
        # Danh sách các nhóm tuổi
        self.age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', 
                        '(38-43)', '(48-53)', '(60-100)']
        
        # Cấu hình
        self.conf_threshold = 0.7
        
    def detect_faces(self, image):
        """Phát hiện khuôn mặt trong ảnh"""
        (h, w) = image.shape[:2]
        
        # Tạo blob từ ảnh
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123])
        
        # Đưa blob vào network
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.conf_threshold:
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                
                faces.append([x1, y1, x2, y2])
                
        return faces
    
    def predict_age(self, face_img):
        """Dự đoán độ tuổi từ ảnh khuôn mặt"""
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), 
                                    (78.4263377603, 87.7689143744, 114.895847746), 
                                    swapRB=False)
        
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        age_index = age_preds[0].argmax()
        
        return self.age_list[age_index]
    
    def process_image(self, image):
        """Xử lý ảnh: phát hiện khuôn mặt và ước tính độ tuổi"""
        # Chuyển đổi sang RGB nếu cần
        if len(image.shape) == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
            
        # Phát hiện khuôn mặt
        faces = self.detect_faces(image)
        
        results = []
        for (x1, y1, x2, y2) in faces:
            # Cắt khuôn mặt
            face = image[y1:y2, x1:x2]
            
            if face.size > 0:
                # Dự đoán độ tuổi
                age = self.predict_age(face)
                results.append({
                    'bbox': (x1, y1, x2, y2),
                    'age': age
                })
                
                # Vẽ bounding box và tuổi
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'Age: {age}', (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return image, results

def download_models():
    """Tải xuống các model cần thiết"""
    import urllib.request
    
    # Tạo thư mục models nếu chưa có
    if not os.path.exists('models'):
        os.makedirs('models')
    
    models = {
        'opencv_face_detector_uint8.pb': 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/opencv_face_detector_uint8.pb',
        'opencv_face_detector.pbtxt': 'https://github.com/opencv/opencv/raw/master/samples/dnn/face_detector/opencv_face_detector.pbtxt',
        'age_deploy.prototxt': 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/age_deploy.prototxt',
        'age_net.caffemodel': 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/age_net.caffemodel'
    }
    
    for filename, url in models.items():
        filepath = f'models/{filename}'
        if not os.path.exists(filepath):
            st.info(f'Đang tải xuống {filename}...')
            try:
                urllib.request.urlretrieve(url, filepath)
                st.success(f'Đã tải xuống {filename}')
            except Exception as e:
                st.error(f'Lỗi khi tải {filename}: {str(e)}')
                return False
    
    return True

def main():
    st.set_page_config(
        page_title="Ứng dụng Nhận diện Tuổi",
        page_icon="👤",
        layout="wide"
    )
    
    st.title("🎯 Ứng dụng Nhận diện Khuôn mặt và Ước tính Độ tuổi")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Cài đặt")
    
    # Kiểm tra và tải models
    if not all(os.path.exists(f'models/{f}') for f in ['opencv_face_detector_uint8.pb', 
                                                       'opencv_face_detector.pbtxt',
                                                       'age_deploy.prototxt', 
                                                       'age_net.caffemodel']):
        st.warning("⚠️ Cần tải xuống các model cần thiết")
        if st.button("📥 Tải xuống Models"):
            if download_models():
                st.success("✅ Đã tải xuống tất cả models!")
                st.experimental_rerun()
        return
    
    # Khởi tạo detector
    try:
        detector = FaceAgeDetector()
    except Exception as e:
        st.error(f"❌ Lỗi khởi tạo detector: {str(e)}")
        return
    
    # Chọn nguồn input
    input_type = st.sidebar.selectbox(
        "📷 Chọn nguồn ảnh:",
        ["Camera trực tiếp", "Tải ảnh lên", "Ảnh mẫu"]
    )
    
    if input_type == "Camera trực tiếp":
        st.subheader("📹 Camera trực tiếp")
        
        # Tạo placeholder cho video
        video_placeholder = st.empty()
        
        # Nút bắt đầu/dừng camera
        col1, col2 = st.columns(2)
        
        with col1:
            start_camera = st.button("▶️ Bắt đầu Camera")
        
        with col2:
            stop_camera = st.button("⏹️ Dừng Camera")
        
        if start_camera:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Không thể mở camera!")
                return
            
            # Session state để điều khiển camera
            if 'camera_running' not in st.session_state:
                st.session_state.camera_running = True
            
            while st.session_state.camera_running:
                ret, frame = cap.read()
                
                if not ret:
                    st.error("❌ Không thể đọc frame từ camera!")
                    break
                
                # Xử lý frame
                processed_frame, results = detector.process_image(frame.copy())
                
                # Hiển thị kết quả
                processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(processed_frame_rgb, channels="RGB", use_column_width=True)
                
                # Hiển thị thông tin
                if results:
                    info_text = f"🔍 Phát hiện {len(results)} khuôn mặt: "
                    for i, result in enumerate(results):
                        info_text += f"Người {i+1}: {result['age']} tuổi "
                    st.info(info_text)
            
            cap.release()
        
        if stop_camera:
            st.session_state.camera_running = False
    
    elif input_type == "Tải ảnh lên":
        st.subheader("📤 Tải ảnh lên")
        
        uploaded_file = st.file_uploader(
            "Chọn ảnh để phân tích:",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Hỗ trợ các định dạng: JPG, JPEG, PNG, BMP"
        )
        
        if uploaded_file is not None:
            # Đọc ảnh
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # Chuyển đổi RGB sang BGR cho OpenCV
            if len(image_np.shape) == 3:
                image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            else:
                image_cv = image_np
            
            # Hiển thị ảnh gốc
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📷 Ảnh gốc")
                st.image(image, use_column_width=True)
            
            # Xử lý ảnh
            with st.spinner("🔄 Đang phân tích..."):
                processed_image, results = detector.process_image(image_cv)
                processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.subheader("🎯 Kết quả phân tích")
                st.image(processed_image_rgb, use_column_width=True)
            
            # Hiển thị thông tin chi tiết
            if results:
                st.success(f"✅ Phát hiện {len(results)} khuôn mặt!")
                
                for i, result in enumerate(results):
                    st.info(f"👤 **Người {i+1}:** Độ tuổi ước tính **{result['age']}**")
            else:
                st.warning("⚠️ Không phát hiện khuôn mặt nào trong ảnh!")
    
    else:  # Ảnh mẫu
        st.subheader("🖼️ Ảnh mẫu")
        st.info("💡 Tính năng này sẽ được bổ sung trong phiên bản tiếp theo")

if __name__ == "__main__":
    main()
