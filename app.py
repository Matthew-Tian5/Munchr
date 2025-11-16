import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import io
from PIL import Image
from reading_functions import getFoodData, readFoodJson, getUserInput, getSuggestion
from container_classes import food, user_request


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

    budget = request.form.get('budget', type=float)
    caloric_budget = request.form.get('caloric_budget', type=float)

    nutrition_concerns = {
        'sugar': request.form.get('sugar_concern', 'false').lower() == 'true',
        'protein': request.form.get('protein_concern', 'false').lower() == 'true',

        'fiber': request.form.get('fiber_concern', 'false').lower() == 'true'
    }

    try:
       
        prompt = """
        Analyze this food image and return ONLY a JSON object with the following structure:
        {
            "name": "food name",
            "calories": estimated_calories,
            "price": estimated_price,
            "fiber": estimated_fiber_grams,
            "protein": estimated_protein_grams,
            "sugar": estimated_sugar_grams
        }
        
        Provide realistic estimates based on typical serving sizes. Return ONLY the JSON, no additional text.
        """
        image = Image.open(image_file.stream)


        response = model.generate_content([prompt, image])
        response_text = response.text.strip()

        #after testing we found that sometimes the response is wrapped in ```json ... ``` so we need to clean that up
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]


        food_data = json.loads(response_text)



        analyzed_food = food(
            name=food_data["name"],
            calories=food_data["calories"],
            price=food_data["price"],
            fiber=food_data["fiber"],
            protein=food_data["protein"],
            sugar=food_data["sugar"]
        )

        user_request_obj = user_request(
            budget=budget,
            food_obj=analyzed_food,
            caloricBudget=caloric_budget,
            nutritionconcerns=nutrition_concerns
        )


        suggestion_data = getSuggestion(user_request_obj)
        suggestion_json = json.loads(suggestion_data)



        #this si for the 2nd part after we give analyze their food
        improvement_prompt = f"""
        Based on this food analysis and user preferences, suggest a healthier/better alternative:
        
        Current Food: {suggestion_json['oldfood']}
        User Concerns: 
        - Budget concern: {suggestion_json['goodPrice']}
        - Calorie concern: {suggestion_json['tooManyCalories']}
        - Nutrition concern: {suggestion_json['poorNutrition']}
        
        Provide 2-3 specific alternative food suggestions that address the user's concerns.

        also give a local store with prices where the user can buy these foods
        Return as a JSON array with objects containing: name, calories, price, fiber, protein, sugar, and reasoning.
        """





        improvement_response = model.generate_content(improvement_prompt)
        improvement_suggestions = json.loads(improvement_response.text)

        return jsonify({
            "analyzed_food": suggestion_json['oldfood'],
            "concerns": {
                "price_issue": suggestion_json['goodPrice'],
                "calorie_issue": suggestion_json['tooManyCalories'],
                "nutrition_issue": suggestion_json['poorNutrition']
            },
            "improvement_suggestions": improvement_suggestions
        })

        


    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Failed to analyze image"}), 500



@app.route("/suggest", methods=["POST"])
def get_food_suggestions():
    """Get food suggestions based on user preferences without an image."""
    try:
        data = request.get_json()
        
       
        mock_food = food(
            name=data.get('current_food', 'generic food'),
            calories=data.get('current_calories', 0),
            price=data.get('current_price', 0),
            fiber=data.get('current_fiber', 0),
            protein=data.get('current_protein', 0),
            sugar=data.get('current_sugar', 0)
        )
        
       
        user_request_obj = user_request(
            budget=data.get('budget', 0),
            food_obj=mock_food,
            caloricBudget=data.get('caloric_budget', 0),
            nutritionconcerns=data.get('nutrition_concerns', {})
        )
        
  
        suggestion_prompt = f"""
        The user wants alternatives to their current food:
        Current Food: {mock_food.name_}
        Calories: {mock_food.calories_}
        Price: ${mock_food.price_}
        Nutrition: {mock_food.nutrition}
        
        User Preferences:
        Budget: ${data.get('budget', 0)}
        Caloric Budget: {data.get('caloric_budget', 0)} calories
        Nutrition Concerns: {data.get('nutrition_concerns', {})}
        
        Provide 3 alternative food suggestions as a JSON array with objects containing:
        name, calories, price, fiber, protein, sugar, and reasoning.
        """
        
        response = model.generate_content(suggestion_prompt)
        suggestions = json.loads(response.text)
        
        return jsonify({"suggestions": suggestions})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True) 