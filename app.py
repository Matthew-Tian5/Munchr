import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import io
from PIL import Image
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    print("Analyze endpoint hit")  # Debug log
    
    if 'image' not in request.files:
        print("No image file in request")  # Debug log
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    
    if image_file.filename == '':
        print("Empty filename")  # Debug log
        return jsonify({"error": "No image file selected"}), 400

    print(f"Processing image: {image_file.filename}")  # Debug log

    try:
        # Get form data
        user_message = request.form.get('message', 'Tell me about this food')
        dietary_preferences = {
            'gluten_free': request.form.get('gluten_free') == 'on',
            'vegetarian': request.form.get('vegetarian') == 'on',
            'vegan': request.form.get('vegan') == 'on',
            'dairy_free': request.form.get('dairy_free') == 'on',
            'allergens': request.form.get('allergens', '')
        }

        print(f"User message: {user_message}")  # Debug log
        print(f"Dietary preferences: {dietary_preferences}")  # Debug log

        # Build the prompt based on user input and dietary preferences
        prompt = build_prompt(user_message, dietary_preferences)
        print(f"Prompt: {prompt}")  # Debug log
        
        # Process the image
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        print("Calling Gemini API...")  # Debug log
        # Generate content using Gemini
        response = model.generate_content([prompt, image])
        
        print("Gemini API call successful")  # Debug log
        
        return jsonify({
            "success": True,
            "analysis": response.text,
            "dietary_info": get_dietary_info(dietary_preferences)
        })

    except Exception as e:
        print(f"Error processing image: {e}")  # Debug log
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Handles follow-up questions about the food."""
    print("Chat endpoint hit")  # Debug log
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get('message', '')
        food_context = data.get('food_context', '')
        
        print(f"Chat - User message: {user_message}")  # Debug log
        print(f"Chat - Food context length: {len(food_context)}")  # Debug log
        
        # Use a text-only model for follow-up questions
        text_model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Based on this food context: {food_context}
        
        User's question: {user_message}
        
        Please provide a helpful response about the food, focusing on:
        - Nutritional information
        - Ingredients analysis
        - Dietary considerations
        - Health benefits/concerns
        - Preparation suggestions
        
        Keep your response concise and informative.
        """
        
        response = text_model.generate_content(prompt)
        
        return jsonify({
            "success": True,
            "response": response.text
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")  # Debug log
        return jsonify({"error": f"Failed to process your question: {str(e)}"}), 500

def build_prompt(user_message, dietary_preferences):
    """Build the prompt for Gemini based on user message and dietary preferences."""
    
    dietary_requirements = []
    if dietary_preferences['gluten_free']:
        dietary_requirements.append("gluten-free")
    if dietary_preferences['vegetarian']:
        dietary_requirements.append("vegetarian")
    if dietary_preferences['vegan']:
        dietary_requirements.append("vegan")
    if dietary_preferences['dairy_free']:
        dietary_requirements.append("dairy-free")
    if dietary_preferences['allergens']:
        dietary_requirements.append(f"free from {dietary_preferences['allergens']}")
    
    dietary_text = ""
    if dietary_requirements:
        dietary_text = f"The user is looking for {', '.join(dietary_requirements)} options. "
    
    base_prompt = f"""
    Analyze this food image and provide detailed information about:
    
    1. What food/dish this appears to be
    2. Main ingredients and components
    3. Nutritional content (calories, macronutrients, key vitamins/minerals)
    4. Potential allergens
    5. Health benefits and concerns
    
    {dietary_text}
    
    {f"Additional user question: {user_message}" if user_message else "Please provide a general analysis of this food."}
    
    Also suggest possible substitutes or modifications that would align with the user's dietary preferences.
    
    Format your response in a clear, conversational way that's easy to understand.
    """
    
    return base_prompt

def get_dietary_info(dietary_preferences):
    """Extract relevant dietary information for the frontend."""
    active_preferences = []
    for pref, active in dietary_preferences.items():
        if active and pref != 'allergens':
            active_preferences.append(pref.replace('_', ' '))
    
    if dietary_preferences['allergens']:
        active_preferences.append(f"allergen-free: {dietary_preferences['allergens']}")
    
    return active_preferences

if __name__ == "__main__":
    app.run(debug=True, port=5000)