import requests
import base64
import os

def test_api():
    """Test the background removal API"""
    
    # API endpoint
    url = "http://localhost:5000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    response = requests.get(f"{url}/health")
    print(f"Health check: {response.json()}")
    
    # Test background removal (you need to have an image file)
    image_path = "test_image.jpg"  # Change this to your image path
    
    if os.path.exists(image_path):
        print(f"\nTesting background removal with {image_path}...")
        
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{url}/remove-background", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Background removed.")
            
            # Save the processed image
            if 'processed_image' in result:
                # Extract base64 data
                base64_data = result['processed_image'].split(',')[1]
                image_data = base64.b64decode(base64_data)
                
                # Save to file
                with open('output_white_background.png', 'wb') as f:
                    f.write(image_data)
                print("Processed image saved as 'output_white_background.png'")
        else:
            print(f"Error: {response.json()}")
    else:
        print(f"Image file '{image_path}' not found. Please add an image file to test.")

if __name__ == "__main__":
    test_api()