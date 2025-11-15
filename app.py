import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import io
import frontend


app = Flask(__name__)


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
       
        prompt = "" #add the prompt made in the json file here 

        #this is for the pictures, modify it as needed for the json file 
        image = Image.open(image_file.stream)
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        


    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Failed to analyze image"}), 500



if __name__ == "__main__":
    app.run(debug=True) 