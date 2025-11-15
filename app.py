import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

# --- Configuration ---
app = Flask(__name__)

# Configure the Gemini API key
# (Make sure to set this as an environment variable!)
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit()


model = genai.GenerativeModel('gemini-pro-vision')


@app.route("/")
def home():
    """Serves the main HTML page."""

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_image():
    """Handles the image upload and Gemini API call."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    try:
       
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        prompt = "Analyze this food picture. What is it? Estimate its calories, nutrition and list the main ingredients."

        # Send image and prompt to Gemini
        response = model.generate_content([prompt, img])
        
        # Return the text response as JSON
        return jsonify({"description": response.text})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Failed to analyze image"}), 500


# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True) # debug=True reloads the server on code changes