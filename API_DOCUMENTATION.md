# 🔌 REST API Documentation - Image Background Remover

## Base URL
```
http://localhost:5000
```

## 📋 API Endpoints

### 1. **GET /** - API Information
Get basic information about the API and available endpoints.

**Request:**
```http
GET /
Content-Type: application/json
```

**Response:**
```json
{
  "message": "Image Background Remover API",
  "endpoints": {
    "/remove-background": "POST - Upload image to remove background",
    "/health": "GET - Check API health"
  }
}
```

---

### 2. **GET /health** - Health Check
Check if the API is running and healthy.

**Request:**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running!"
}
```

---

### 3. **POST /remove-background** - Remove Background
Upload an image and get it back with background removed and white background applied.

**Request:**
```http
POST /remove-background
Content-Type: multipart/form-data

Form Data:
- image: [binary file] (required)
```

**Supported formats:** PNG, JPG, JPEG, GIF, BMP, WEBP

**Response (Success):**
```json
{
  "success": true,
  "message": "Background removed and replaced with white successfully!",
  "processed_image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "filename": "processed_image_name.png"
}
```

**Response (Error):**
```json
{
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (no file, invalid format, etc.)
- `500` - Internal Server Error

---

### 4. **GET /download/{filename}** - Download File
Download a processed image file.

**Request:**
```http
GET /download/processed_image_name.png
```

**Response:**
- **Success:** Binary file download
- **Error (404):** `{"error": "File not found"}`

---

## 🧪 Testing the REST API

### Using cURL

#### 1. Health Check
```bash
curl -X GET http://localhost:5000/health
```

#### 2. API Information
```bash
curl -X GET http://localhost:5000/
```

#### 3. Remove Background
```bash
curl -X POST \
  -F "image=@/path/to/your/image.jpg" \
  http://localhost:5000/remove-background
```

#### 4. Download File
```bash
curl -X GET http://localhost:5000/download/processed_image.png \
  --output downloaded_image.png
```

### Using Python requests

```python
import requests
import base64

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Remove background
with open('your_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/remove-background', files=files)
    
if response.status_code == 200:
    result = response.json()
    print("Success:", result['message'])
    
    # Save the processed image
    base64_data = result['processed_image'].split(',')[1]
    image_data = base64.b64decode(base64_data)
    
    with open('output_white_bg.png', 'wb') as f:
        f.write(image_data)
    print("Image saved as output_white_bg.png")
else:
    print("Error:", response.json())
```

### Using JavaScript/Fetch

```javascript
// Health check
fetch('http://localhost:5000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Remove background
const fileInput = document.getElementById('fileInput');
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/remove-background', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Success:', data.message);
    // Display or download the processed image
    const img = document.createElement('img');
    img.src = data.processed_image;
    document.body.appendChild(img);
  } else {
    console.error('Error:', data.error);
  }
});
```

---

## 🔧 Error Handling

### Common Error Responses

**No image provided:**
```json
{
  "error": "No image file provided"
}
```

**No file selected:**
```json
{
  "error": "No file selected"
}
```

**Invalid file type:**
```json
{
  "error": "Invalid file type. Supported: PNG, JPG, JPEG, GIF, BMP, WEBP"
}
```

**Processing failed:**
```json
{
  "error": "Processing failed: [specific error reason]"
}
```

**File not found:**
```json
{
  "error": "File not found"
}
```

---

## 🚀 Quick Start

1. **Start the API server:**
   ```bash
   ./start_server.sh
   ```

2. **Test with curl:**
   ```bash
   curl http://localhost:5000/health
   ```

3. **Remove background:**
   ```bash
   curl -X POST -F "image=@your_image.jpg" http://localhost:5000/remove-background
   ```

---

## 🔒 CORS Support

The API includes CORS headers, so you can call it from web browsers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

---

## 📊 Response Format

All responses are in JSON format except for file downloads.

**Success Response Structure:**
```json
{
  "success": true,
  "message": "Success message",
  "processed_image": "base64_encoded_image_data",
  "filename": "output_filename.png"
}
```

**Error Response Structure:**
```json
{
  "error": "Error description"
}
```

---

## 🎯 Integration Examples

### React/Next.js
```jsx
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);
  
  try {
    const response = await fetch('http://localhost:5000/remove-background', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    if (data.success) {
      setProcessedImage(data.processed_image);
    }
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

### Vue.js
```javascript
async uploadImage(file) {
  const formData = new FormData();
  formData.append('image', file);
  
  try {
    const response = await this.$http.post('/remove-background', formData);
    this.processedImage = response.data.processed_image;
  } catch (error) {
    console.error('Upload failed:', error);
  }
}
```

### Angular
```typescript
uploadImage(file: File): Observable<any> {
  const formData = new FormData();
  formData.append('image', file);
  
  return this.http.post<any>('/remove-background', formData);
}
```

This REST API is production-ready and can be integrated into any application that can make HTTP requests!