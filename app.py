from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from PIL import Image
import io
import base64
from rembg import remove
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Create upload folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({
        "message": "Image Background Remover API",
        "endpoints": {
            "/remove-background": "POST - Upload image to remove background",
            "/health": "GET - Check API health"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "API is running!"})

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({"error": "Invalid file type. Supported: PNG, JPG, JPEG, GIF, BMP, WEBP"}), 400
        
        # Read the image
        input_image = Image.open(file.stream)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
        
        # Remove background using rembg
        output_image = remove(input_image)
        
        # Create white background
        white_bg = Image.new('RGB', output_image.size, (255, 255, 255))
        
        # Paste the image with removed background onto white background
        white_bg.paste(output_image, mask=output_image.split()[-1])  # Use alpha channel as mask
        
        # Save processed image
        output_filename = f"processed_{file.filename.rsplit('.', 1)[0]}.png"
        output_path = os.path.join(PROCESSED_FOLDER, output_filename)
        white_bg.save(output_path, 'PNG')
        
        # Convert to base64 for response
        img_buffer = io.BytesIO()
        white_bg.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "message": "Background removed and replaced with white successfully!",
            "processed_image": f"data:image/png;base64,{img_base64}",
            "filename": output_filename
        })
        
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed image"""
    try:
        file_path = os.path.join(PROCESSED_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Image Background Remover API...")
    print("Available endpoints:")
    print("- GET  /          : API information")
    print("- GET  /health    : Health check")
    print("- POST /remove-background : Upload image to remove background")
    print("- GET  /download/<filename> : Download processed image")
    print("\nAPI running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)