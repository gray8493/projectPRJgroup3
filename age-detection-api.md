# Hướng dẫn tích hợp API nhận diện tuổi thật

## API hiện tại (Demo)
Hiện tại hệ thống sử dụng hàm `simulateAgeDetection()` để mô phỏng việc nhận diện tuổi. Để tích hợp API thật, bạn cần thay thế hàm này.

## Các API nhận diện tuổi phổ biến

### 1. Azure Face API (Microsoft)
```javascript
async function detectAgeWithAzure(imageData) {
  const subscriptionKey = 'YOUR_AZURE_KEY';
  const endpoint = 'YOUR_AZURE_ENDPOINT';
  
  const response = await fetch(`${endpoint}/face/v1.0/detect?returnFaceAttributes=age`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscriptionKey
    },
    body: imageData
  });
  
  const data = await response.json();
  return data[0]?.faceAttributes?.age || 25;
}
```

### 2. AWS Rekognition
```javascript
async function detectAgeWithAWS(imageData) {
  const AWS = require('aws-sdk');
  const rekognition = new AWS.Rekognition();
  
  const params = {
    Image: { Bytes: imageData },
    Attributes: ['AGE_RANGE']
  };
  
  const result = await rekognition.detectFaces(params).promise();
  const ageRange = result.FaceDetails[0]?.AgeRange;
  return Math.floor((ageRange.Low + ageRange.High) / 2);
}
```

### 3. Google Cloud Vision API
```javascript
async function detectAgeWithGoogle(imageData) {
  const response = await fetch(`https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      requests: [{
        image: { content: imageData.split(',')[1] },
        features: [{ type: 'FACE_DETECTION' }]
      }]
    })
  });
  
  const data = await response.json();
  const face = data.responses[0]?.faceAnnotations?.[0];
  return face?.joyLikelihood === 'VERY_LIKELY' ? 25 : 30;
}
```

## Cách thay thế trong menu.html

Thay thế hàm `simulateAgeDetection` trong file `menu.html`:

```javascript
// Thay thế hàm này:
function simulateAgeDetection(imageData){
  return new Promise((resolve) => {
    setTimeout(() => {
      const ages = [8, 15, 22, 28, 35, 45, 55];
      const randomAge = ages[Math.floor(Math.random() * ages.length)];
      resolve(randomAge);
    }, 2000);
  });
}

// Bằng hàm API thật:
async function detectAgeWithAPI(imageData){
  try {
    // Chuyển đổi base64 thành blob
    const response = await fetch(imageData);
    const blob = await response.blob();
    
    // Gọi API nhận diện tuổi
    const formData = new FormData();
    formData.append('image', blob);
    
    const apiResponse = await fetch('YOUR_API_ENDPOINT', {
      method: 'POST',
      body: formData
    });
    
    const result = await apiResponse.json();
    return result.age; // Trả về tuổi từ API
    
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Không thể nhận diện tuổi');
  }
}
```

## Cập nhật hàm analyzeAge

```javascript
async function analyzeAge(){
  if(!capturedImageData) return;
  
  const analyzeBtn = document.getElementById('analyzeBtn');
  analyzeBtn.textContent = '⏳ Đang phân tích...';
  analyzeBtn.disabled = true;
  
  try {
    // Thay đổi từ simulateAgeDetection sang detectAgeWithAPI
    const age = await detectAgeWithAPI(capturedImageData);
    
    document.getElementById('ageResult').textContent = `Độ tuổi ước tính: ${age} tuổi`;
    document.getElementById('cameraPreview').style.display = 'none';
    document.getElementById('cameraResult').style.display = 'block';
    
  } catch (error) {
    console.error('Age detection failed:', error);
    alert('Không thể phân tích tuổi. Vui lòng thử lại hoặc chọn thủ công.');
  } finally {
    analyzeBtn.textContent = '🔍 Phân tích tuổi';
    analyzeBtn.disabled = false;
  }
}
```

## Lưu ý bảo mật

1. **API Keys**: Không để API keys trong frontend code. Sử dụng backend proxy.
2. **HTTPS**: Camera chỉ hoạt động trên HTTPS hoặc localhost.
3. **Privacy**: Thông báo cho người dùng về việc sử dụng camera và phân tích hình ảnh.

## Backend Proxy (Khuyến nghị)

Tạo một API endpoint trên server của bạn:

```javascript
// server.js (Node.js example)
app.post('/api/detect-age', upload.single('image'), async (req, res) => {
  try {
    const imageBuffer = req.file.buffer;
    
    // Gọi API nhận diện tuổi
    const age = await callAgeDetectionAPI(imageBuffer);
    
    res.json({ age, success: true });
  } catch (error) {
    res.status(500).json({ error: 'Detection failed' });
  }
});
```

Sau đó gọi từ frontend:

```javascript
async function detectAgeWithAPI(imageData){
  const formData = new FormData();
  formData.append('image', imageData);
  
  const response = await fetch('/api/detect-age', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  return result.age;
}
```

## Test và Debug

1. Kiểm tra console để xem lỗi API
2. Test với nhiều hình ảnh khác nhau
3. Xử lý trường hợp không nhận diện được khuôn mặt
4. Thêm fallback về chọn tuổi thủ công khi API lỗi
