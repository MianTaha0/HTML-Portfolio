# 🚀 Quick Start Guide - Image Background Remover

## ⚡ Super Fast Setup (3 steps!)

### 1. Start the Server
```bash
./start_server.sh
```

### 2. Open the Web Interface
- Open `frontend.html` in your web browser
- Or visit: `http://localhost:5000` (after server starts)

### 3. Remove Backgrounds!
- Drag and drop an image, or click to browse
- Wait for processing (first time takes longer)
- Download your image with white background!

---

## 🛠️ Manual Setup (if needed)

If the quick start doesn't work, follow these steps:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install Flask Flask-CORS Pillow rembg numpy requests
```

### 3. Run the Server
```bash
python app.py
```

---

## 🧪 Test the API

### Using the Web Interface
1. Open `frontend.html` in your browser
2. Upload an image
3. Download the result

### Using curl (for developers)
```bash
# Health check
curl http://localhost:5000/health

# Remove background (replace with your image path)
curl -X POST -F "image=@your_image.jpg" http://localhost:5000/remove-background
```

### Using Python Script
```bash
python test_api.py
```
*(Make sure you have a test image named `test_image.jpg` in the folder)*

---

## 🎯 API Endpoints

- `GET /` - API information
- `GET /health` - Check if API is running  
- `POST /remove-background` - Upload image to remove background
- `GET /download/<filename>` - Download processed image

---

## 🐛 Troubleshooting

### Server won't start?
1. Check Python version: `python3 --version` (need 3.7+)
2. Try: `pip install --upgrade pip`
3. Install system packages: `sudo apt install python3-venv python3-pip`

### First processing is slow?
- This is normal! The AI model downloads on first use (~176MB)
- Subsequent processing will be much faster

### Can't access the web interface?
1. Make sure the server is running on `http://localhost:5000`
2. Try opening `frontend.html` directly in your browser
3. Check that no firewall is blocking port 5000

### Memory issues?
- Try smaller images (under 2MB work best)
- Close other applications to free up RAM

---

## 💡 Tips for Best Results

- **Image formats**: PNG, JPG, JPEG work best
- **Image size**: Smaller images (under 2MB) process faster
- **Subject clarity**: Clear subject separation from background works better
- **Lighting**: Well-lit images with good contrast give better results

---

## 🎨 Customization

Want a different background color? Edit `app.py` line 59:
```python
# Change from white (255, 255, 255) to any RGB color
white_bg = Image.new('RGB', output_image.size, (0, 100, 255))  # Blue background
```

---

## 🆘 Need Help?

1. Check the full README.md for detailed information
2. Make sure all files are in the same directory
3. Verify virtual environment is activated
4. Read error messages carefully - they usually explain the issue

**Happy background removing! 🖼️✨**