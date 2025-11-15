#This class stores information about a food the user is either suggested or buys
class food:
    #CONSTRUCTOR
    def __init__(self, name, calories, price, fiber, protein, sugar):
        #store the basic food information
        self.calories_ = calories
        self.price_ = price
        self.name_ = name
        #create a dictionary to store the macronutrients. we can easily add more later
        self.nutrition = {}
        self.nutrition["fiber"] = fiber
        self.nutrition["protein"] = protein
        self.nutrition["sugar"] = sugar
    #this function returns whether or not something is high in sugar
    #if it is high in sugar then the calories from sugar is over 
    def isHighSugar(self):
        #4 calories per gram of sugar
        return (self.nutrition["sugar"]*4) / self.calories
    def isHighFiber(self):
        #20 grams of fiber per 1000 calories is a good ratio
        return self.nutrition["fiber"]/.02 > 1000
    def isHighProtein(self):
        #4 calories per gram of protein
        return self.nutrition["protein"]*4 > calories*.35
    def getPrice(self):
        return self.price_
    def getCalories(self):
        return self.calories_


class user_request:
    #CONSTRUCTOR
    def __init__(self, budget, food, caloricBudget, nutritionconcerns):
        #store the information about the user's request
        self.original_food_ = food
        self.monetary_budget_ = budget
        self.caloric_budget_ = caloricBudget
        #in concerns the concern for each variable, low sugar, protein, and fiber will be stored
        #so that the ai can make a reasonable prediction based on the concern for each
        self.concerns_ = nutritionconcerns
    #this snippet of code checks for any mismatches between the user's desires and the nutritional content
    def nutritionalMatch(self):
        if self.original_food_.isHighFiber() and nutritionconcerns["fiber"]:
            return False
        if self.original_food_.isHighSugar() and nutritionconcerns["sugar"]:
            return False
        if self.original_food_.isHighProtein() and nutritionconcerns["protein"]:
            return True
        return True
    #this returns whether the food is in the user's budget
    def requestExpensive(self):
        return self.monetary_budget_ <= self.original_food_.getPrice()
    def overCaloricBudget(self):
        return self.caloric_budget_ <= self.original_food_.getCalories()
    
    