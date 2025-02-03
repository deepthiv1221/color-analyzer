from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's local server URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Color Analyzer API!"}

def rgb_to_hex(rgb):
    """Convert an RGB tuple to a HEX color string."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

@app.post("/analyze/")
async def analyze_color(file: UploadFile = File(...)):
    try:
        # Read image from the uploaded file
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        # Convert image to RGB and then to numpy array
        image_rgb = np.array(image.convert("RGB"))

        # Calculate the average color
        avg_color = image_rgb.mean(axis=(0, 1)).astype(int)  
        avg_hex = rgb_to_hex(tuple(avg_color))

        # Example logic for best/worst colors based on brightness
        brightness = sum(avg_color) / 3
        best_color = "#FFFFFF" if brightness < 128 else "#000000"
        worst_color = "#000000" if brightness < 128 else "#FFFFFF"

        return JSONResponse(content={
            "message": "Color analysis successful!",
            "average_color": {
                "r": int(avg_color[0]), 
                "g": int(avg_color[1]), 
                "b": int(avg_color[2]),
                "hex": avg_hex
            },
            "best_color": best_color,
            "worst_color": worst_color
        })
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
