from container_classes import *
import json

#get food data is now done in app.py

#read in the json file and then using that json file we then return an object containing the recovered info
def readFoodJson(foodJson):
    readJson = json.load(foodJson)
    return food(readJson["name"], readJson["calories"], readJson["price"], readJson["fiber"], readJson["protein"], readJson["sugar"])
#read in the request and only return the tuple of information rather than an object
def readReqJsonData(requestFile):
    readJson = json.load(requestFile)
    return (readJson["budget"], readJson["caloricBudget"], 
            {"fiber":readJson["nutritionconcerns"]["fiber"],
             "sugar":readJson["nutritionconcerns"]["sugar"], 
             "protein":readJson["nutritionconcerns"]["protein"]})

#returns an object containing information about the user's request that is used by gemini to give them feedback
def getUserInput(food, userRequestJson):
    budget, caloricBudget, nutritionconcerns = readReqJsonData(userRequestJson)
    #convert the user input into an object
    userInput = user_request(budget, food_obj, caloricBudget, nutritionconcerns) 

    return userInput

def getSuggestion(userRequest):
    originalFood = userRequest.getOriginalFood()
    #create a json object of information for AI
    request_info = {
        "oldfood":{
            "name": originalFood.name_,
            "calories" : originalFood.getCalories(),
            "price" : originalFood.getPrice(),
            "fiber" : originalFood.getNutrition()["fiber"],
            "protein" : originalFood.getNutrition()["protein"],
            "sugar" : originalFood.getNutrition()["sugar"]
        },
        "goodPrice": userRequest.requestExpensive(),
        "tooManyCalories": userRequest.overCaloricBudget(),
        "poorNutrition": userRequest.nutritionalMatch()
    }
    suggestionRequestJson = json.dumps(request_info)

    #feed the json object
    #return the 
    return suggestionRequestJson

if __name__ == "__main__":
    #get our food object by feeding in our food json
    Food = readFoodJson(open('/Users/jstevethom/VSCProjects/HackRPIMunchr/Munchr/backend/exampleFood.json', 'r'))
    #now get our user input object by feeding in our user input and the food object
    Req = getUserInput(food, open('/Users/jstevethom/VSCProjects/HackRPIMunchr/Munchr/backend/exampleRequest.json', 'r'))
    #now we finally get a suggestion json
    suggest = getSuggestion(Req)
    print(suggest)


