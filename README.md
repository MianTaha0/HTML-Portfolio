# Image Background Remover API

A simple Python Flask backend for removing image backgrounds and replacing them with white backgrounds. This project is beginner-friendly and uses the `rembg` library for AI-powered background removal.

## Features

- 🖼️ Remove backgrounds from images using AI
- ⚪ Replace background with white color
- 🌐 RESTful API with Flask
- 📱 Beautiful web interface for testing
- 🔄 Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, WEBP)
- 📥 Download processed images
- 🎯 CORS enabled for frontend integration

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## Usage

### Option 1: Web Interface (Recommended for beginners)

1. Start the Flask server (`python app.py`)
2. Open `frontend.html` in your web browser
3. Drag and drop an image or click to browse
4. Wait for processing (usually 5-15 seconds)
5. Download the processed image with white background

### Option 2: API Endpoints

#### Health Check
```
GET http://localhost:5000/health
```

#### Remove Background
```
POST http://localhost:5000/remove-background
Content-Type: multipart/form-data

Form data:
- image: [image file]
```

**Response:**
```json
{
  "success": true,
  "message": "Background removed and replaced with white successfully!",
  "processed_image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "filename": "processed_image.png"
}
```

#### Download File
```
GET http://localhost:5000/download/<filename>
```

### Option 3: Test Script

Run the test script to test the API programmatically:

```bash
# Make sure you have a test image named 'test_image.jpg' in the project folder
python test_api.py
```

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check |
| POST | `/remove-background` | Upload image to remove background |
| GET | `/download/<filename>` | Download processed image |

### Error Responses

```json
{
  "error": "Error message description"
}
```

Common errors:
- `No image file provided` (400)
- `No file selected` (400) 
- `Invalid file type` (400)
- `Processing failed: [reason]` (500)

## File Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── frontend.html       # Web interface for testing
├── test_api.py        # Test script
├── README.md          # This file
├── uploads/           # Uploaded images (created automatically)
└── processed/         # Processed images (created automatically)
```

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Pillow**: Image processing
- **rembg**: AI background removal
- **numpy**: Numerical operations
- **requests**: HTTP library (for testing)

## Troubleshooting

### Common Issues

1. **"No module named 'rembg'" error**
   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **Slow first processing**
   - The first image processing might be slow as rembg downloads the AI model (about 176MB)
   - Subsequent processing will be much faster

3. **API connection error in frontend**
   - Make sure the Flask server is running on localhost:5000
   - Check that CORS is enabled (it's included in the code)

4. **Memory issues with large images**
   - Try resizing your images to smaller dimensions before processing
   - The API can handle most common image sizes

### Performance Tips

- Smaller images (under 2MB) process faster
- PNG format often gives better results than JPEG
- The first run downloads the AI model, subsequent runs are faster

## Customization

### Change Background Color

To change the white background to another color, modify line 59 in `app.py`:

```python
# Change (255, 255, 255) to your desired RGB color
white_bg = Image.new('RGB', output_image.size, (255, 255, 255))  # White
# Example for blue background:
# blue_bg = Image.new('RGB', output_image.size, (0, 100, 255))  # Blue
```

### Add More File Formats

Add more formats to the `allowed_extensions` set in `app.py` line 44:

```python
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
```

## License

This project is for educational purposes. The `rembg` library has its own license terms.

## Support

For beginners:
1. Make sure Python is installed correctly
2. Use a virtual environment for cleaner dependency management
3. Check that all files are in the same directory
4. Read error messages carefully - they usually explain the issue

If you encounter issues, check:
- Python version (3.7+)
- All dependencies installed
- Flask server is running
- File permissions for upload/processed folders