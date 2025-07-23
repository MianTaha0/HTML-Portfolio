"""
Image Background Remover REST API
A simple Flask REST API for removing image backgrounds and replacing with white background.
Pure API - no frontend included.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from PIL import Image
import io
import base64
from rembg import remove
import tempfile
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
PROCESSED_FOLDER = 'processed_images'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Create directories
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename():
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"processed_{timestamp}_{unique_id}.png"

# ===== REST API ENDPOINTS =====

@app.route('/', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        "name": "Image Background Remover API",
        "version": "1.0.0",
        "description": "REST API for removing image backgrounds and replacing with white background",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /api/remove-background": "Upload image to remove background",
            "GET /api/download/<filename>": "Download processed image",
            "GET /api/status": "API status and statistics"
        },
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Image Background Remover API is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status with statistics"""
    try:
        processed_files = len([f for f in os.listdir(PROCESSED_FOLDER) if f.endswith('.png')])
    except:
        processed_files = 0
    
    return jsonify({
        "status": "operational",
        "uptime": "running",
        "processed_images_count": processed_files,
        "available_space": True,
        "ai_model": "rembg",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/remove-background', methods=['POST', 'OPTIONS'])
def remove_background_api():
    """Main API endpoint for background removal"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight successful"}), 200
    
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({
                "error": "No image file provided",
                "code": "NO_FILE"
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                "error": "No file selected",
                "code": "EMPTY_FILE"
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Invalid file type. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}",
                "code": "INVALID_FORMAT",
                "supported_formats": list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "error": f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB",
                "code": "FILE_TOO_LARGE",
                "max_size_mb": MAX_FILE_SIZE // (1024*1024)
            }), 400
        
        # Process image
        input_image = Image.open(file.stream)
        
        # Convert to RGB if necessary
        if input_image.mode in ('RGBA', 'P'):
            # Keep transparency information for processing
            pass
        elif input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
        
        # Remove background using rembg
        output_image = remove(input_image)
        
        # Create white background
        white_bg = Image.new('RGB', output_image.size, (255, 255, 255))
        
        # Paste the image with removed background onto white background
        if output_image.mode == 'RGBA':
            white_bg.paste(output_image, mask=output_image.split()[-1])
        else:
            white_bg.paste(output_image)
        
        # Generate unique filename
        output_filename = generate_filename()
        output_path = os.path.join(PROCESSED_FOLDER, output_filename)
        
        # Save processed image
        white_bg.save(output_path, 'PNG', optimize=True)
        
        # Convert to base64 for API response
        img_buffer = io.BytesIO()
        white_bg.save(img_buffer, format='PNG', optimize=True)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "message": "Background removed and replaced with white successfully",
            "data": {
                "processed_image": f"data:image/png;base64,{img_base64}",
                "filename": output_filename,
                "download_url": f"/api/download/{output_filename}",
                "original_size": file_size,
                "processed_size": len(img_buffer.getvalue()),
                "format": "PNG"
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Processing failed: {str(e)}",
            "code": "PROCESSING_ERROR",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file_api(filename):
    """Download processed image file"""
    try:
        # Security: only allow files in processed folder with .png extension
        if not filename.endswith('.png') or '..' in filename:
            return jsonify({
                "error": "Invalid filename",
                "code": "INVALID_FILENAME"
            }), 400
        
        file_path = os.path.join(PROCESSED_FOLDER, filename)
        
        if os.path.exists(file_path):
            return send_file(
                file_path, 
                as_attachment=True,
                download_name=filename,
                mimetype='image/png'
            )
        else:
            return jsonify({
                "error": "File not found",
                "code": "FILE_NOT_FOUND",
                "filename": filename
            }), 404
            
    except Exception as e:
        return jsonify({
            "error": f"Download failed: {str(e)}",
            "code": "DOWNLOAD_ERROR"
        }), 500

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "code": "NOT_FOUND",
        "available_endpoints": [
            "GET /",
            "GET /health", 
            "GET /api/status",
            "POST /api/remove-background",
            "GET /api/download/<filename>"
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "code": "METHOD_NOT_ALLOWED"
    }), 405

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        "error": f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB",
        "code": "PAYLOAD_TOO_LARGE"
    }), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "code": "INTERNAL_ERROR"
    }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Image Background Remover REST API")
    print("=" * 60)
    print("📡 API Base URL: http://localhost:5000")
    print("🔍 Health Check: http://localhost:5000/health")
    print("📊 API Status: http://localhost:5000/api/status")
    print("🖼️  Remove Background: POST /api/remove-background")
    print("📥 Download: GET /api/download/<filename>")
    print("=" * 60)
    print("⚡ Features:")
    print("  • AI-powered background removal")
    print("  • White background replacement")
    print("  • RESTful API design")
    print("  • CORS enabled")
    print("  • Error handling")
    print("  • File validation")
    print("  • Base64 image responses")
    print("=" * 60)
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)