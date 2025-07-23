# 🌐 How to Use the Background Remover Website

## 🚀 **Super Simple Steps:**

### Step 1: Start the Server
```bash
./start_server.sh
```
*Wait for the message "API running on http://localhost:5000"*

### Step 2: Open the Website
**Choose one of these files:**
- **`simple_website.html`** - Clean, easy interface ⭐ **RECOMMENDED**
- **`frontend.html`** - Full-featured interface

**How to open:**
1. **Double-click** the HTML file, OR
2. **Right-click** → "Open with" → Choose your web browser, OR  
3. **Drag the file** into your browser window

### Step 3: Upload Your Image
1. **Click "Select Image"** or **drag & drop** an image
2. **Wait** for processing (first time takes longer)
3. **Download** your image with white background!

---

## 📱 **What Users Can Do:**

✅ **Upload images** from their computer  
✅ **Drag and drop** images directly  
✅ **See preview** of original and processed images  
✅ **Download** the processed image  
✅ **Upload multiple images** (one at a time)  
✅ **Works on mobile** and desktop  

---

## 🖼️ **Supported Image Types:**
- PNG
- JPG/JPEG
- GIF
- BMP
- WEBP

**File size limit:** 10MB

---

## 🎯 **User Experience:**

### Before Upload:
```
🖼️ Background Remover
Upload any image and get it back with a clean white background

[📸 Choose an image or drag it here]
[Select Image Button]
```

### During Processing:
```
⏳ Removing background...
This may take a few moments
```

### After Processing:
```
✅ Background removed successfully! 🎉

[Original Image]    [White Background]
     📷                   📷

[📥 Download Image] [Upload Another Image]
```

---

## 📋 **Complete Setup Instructions:**

### For Beginners:

1. **Open Terminal/Command Prompt**
2. **Navigate to the project folder**
3. **Run:** `./start_server.sh`
4. **Open** `simple_website.html` in your browser
5. **Upload an image** and enjoy!

### Troubleshooting:

**❌ "API server not running" error?**
- Make sure you ran `./start_server.sh` first
- Wait for "API running on http://localhost:5000" message

**❌ File won't upload?**
- Check file size (must be under 10MB)
- Use supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

**❌ Processing taking too long?**
- First time downloads AI model (~176MB)
- Subsequent uploads will be much faster

---

## 🌍 **Sharing with Others:**

To let others use your website:

1. **Start the server** on your computer
2. **Find your IP address**: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. **Share the link**: `http://YOUR_IP:5000`
4. **Others open** the HTML file in their browser
5. **They upload images** from their devices!

*Note: Your computer must stay on and connected to the internet*

---

## 🔧 **Advanced Options:**

### Change the API URL:
Edit the HTML file and change:
```javascript
const API_URL = 'http://localhost:5000';
```
To your server's address.

### Deploy Online:
- Upload the API to a cloud service (Heroku, Vercel, etc.)
- Update the API_URL in the HTML file
- Host the HTML file on any web server

---

**🎉 That's it! Your users can now remove image backgrounds through a beautiful web interface!**