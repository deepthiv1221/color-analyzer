import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Define color palettes
color_palettes = {
    "warm": ["#FF5733", "#FF8D1A", "#F1C40F", "#F39C12", "#F4D03F", "#FF6347", "#FF4500", "#FF1493", "#FF69B4", "#FFD700"],
    "cool": ["#3498DB", "#1ABC9C", "#9B59B6", "#8E44AD", "#2980B9", "#5DADE2", "#A569BD", "#48C9B0", "#5D6D7E", "#7FB3D5"],
    "pastel": ["#FAD02E", "#F28D35", "#D83367", "#89A8F3", "#A7D8F5", "#F4A261", "#2A9D8F", "#E76F51", "#6C757D", "#B4C8D6"],
    "bright": ["#E63946", "#F1FAEE", "#F1C6B3", "#D84A3B", "#F76C5E", "#FF9F1C", "#FFD23F", "#80FF72", "#00B5D9", "#E94E77"],
    "dull": ["#7D7F7D", "#B4B8B8", "#B0B0B0", "#9C9C9C", "#C2C2C2", "#A9A9A9", "#D3D3D3", "#E6E6E6", "#808080", "#A0A0A0"]
}

# Face detection function using OpenCV
def detect_face_color(image_path):
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return None  # No face detected
    
    # Extract color from the face region
    (x, y, w, h) = faces[0]  # Take the first detected face
    face_region = image[y:y+h, x:x+w]
    
    # Convert to RGB
    face_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
    
    # Calculate the average color in the face region
    avg_color = np.mean(face_rgb, axis=(0, 1))  # average of RGB channels
    
    # Convert avg RGB color to hex
    avg_color_hex = '#{:02x}{:02x}{:02x}'.format(int(avg_color[0]), int(avg_color[1]), int(avg_color[2]))
    
    return avg_color_hex

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/analyze', methods=['POST'])
def analyze_color():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']

    # Save the image file temporarily
    image_path = "uploaded_image.jpg"
    image_file.save(image_path)
    
    # Detect face color
    face_color = detect_face_color(image_path)
    
    if not face_color:
        return jsonify({"error": "No face detected"}), 400
    
    # Get closest matching colors from predefined palettes
    best_matches = get_closest_color(face_color)
    
    return jsonify({"best": best_matches})

def get_closest_color(requested_color):
    def hex_to_rgb(hex):
        return [int(hex[i:i+2], 16) for i in (1, 3, 5)]

    closest_colors = []
    min_distance = float('inf')

    for category, colors in color_palettes.items():
        for color in colors:
            color_rgb = hex_to_rgb(color)
            requested_rgb = hex_to_rgb(requested_color)
            distance = np.sqrt(sum([(requested_rgb[i] - color_rgb[i]) ** 2 for i in range(3)]))

            if distance < min_distance:
                min_distance = distance
                closest_colors.append(color)

    return closest_colors[:10]

if __name__ == '__main__':
    app.run(debug=True)
