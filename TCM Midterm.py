# This program uses the MealDB API to help users find and cook meals.

import requests, json, pprint, sys

# This is the first line of the main code that introduces the User to the program and asks for their name
print("Welcome Chef! What is your name?")
myName = input()

# This is a list of the main ingredients found in the MealDB website.
# This list will be called later to ensure user's only pick a meal that the website has a recipe for.
categoryList = ['beef', 'chicken', 'goat', 'lamb','pork', 'salmon', 'cheese', 'potatoes', 'tomato', 'eggs', 'flour',
                'avocado']

# pickChef is the first function that asks the user whether they know what recipe they'd like to cook.
# If the user knows what recipe they'd like to cook, theRecipe function is called. Otherwise, lostChef is called.
def pickChef():
    picky = ''
    while picky !='yes' and picky != 'no':
        print('Hi ' + myName + '! Do you know what recipe you\'d like to cook? (yes or no)')
        picky = input()

    if picky == 'yes':
        theRecipe()

    if picky == 'no':
        lostChef()

# This function helps users find a meal using the URL that prints all meals that use a certain main ingredient.
def lostChef():
    print('What main ingredient would you like to use?')
    foodType = input()

    if foodType in categoryList:
        print('Here are the recipes using ' + foodType + '.')

        url = 'https://www.themealdb.com/api/json/v1/1/filter.php?i=' + foodType
        response = requests.get(url)
        response.raise_for_status()  # check for errors

        # load json data
        jsonData = json.loads(response.text)
        length = len(jsonData['meals'])
        # This for loop ensures that the program prints all of the recipes for the chosen main ingredient.
        # Each  ingredient has a different number of recipes, which is why the range is set to the variable "length".
        for i in range (0, length):
                mainIngredient = jsonData['meals'][i]
                pprint.pprint(mainIngredient[f'strMeal'])
        print('')
        # Once the User has a list of meals to choose from, the program runs theRecipe,
        # This allows the user to pick one of the meals that was returned to them and receive the recipe to cook it.
        theRecipe()

# The else statement will re-run the lostChef function if the user chooses an ingredient that is not a part of the API.
    else:
        print('Please enter one of the following categories:')
        print(categoryList)
        lostChef()

def satisfiedChef():
    happyCamper = ''
    while happyCamper != 'yes' and happyCamper != 'no':
        print(myName + ', are you satisfied with your recipe (yes or no)')
        happyCamper = input()
        if happyCamper == 'yes':
            print('Great! Bon Appétit ' + myName + '!')
            print('')
            sys.exit()
        if happyCamper == 'no':
            print('Okay, let\'s start over!')
            pickChef()

# This function asks the user what recipe they'd like to cook and returns the recipe to them.
def theRecipe():
    while True:
        try:
                print('Ok, ' + myName + ', which recipe would you like to cook?')
                myRecipe = input()
              
                if len(myRecipe) < 4:
                    print('Please use at least 4 characters.')
                    
                else:


                  url = 'https://www.themealdb.com/api/json/v1/1/search.php?s='+myRecipe
                  response = requests.get(url)
                  response.raise_for_status()  # check for errors

                  # load json data
                  jsonData = json.loads(response.text)
                  # pprint.pprint(jsonData)
                  meal = jsonData['meals'][0]
                  print('Recipe chosen: ' + meal['strMeal'])
                  print('Main ingredient: ' + meal['strCategory'])  # This prints the main ingredient of the meal.
                  # This for loop prints ensures that the program prints all the ingredients and measurements used in the meal.
                  print('Ingredients needed:')
                  for i in range(1,20):
                      if meal[f'strIngredient{i}'] != None:
                          mealInfo = meal[f'strIngredient{i}'] + ' - ' + meal[f'strMeasure{i}']
                          pprint.pprint(mealInfo)
                  # This print statement prints the instructions to cook the meal.
                  print('Cooking instructions:')
                  mealInstruction = meal['strInstructions']
                  pprint.pprint(mealInstruction)
                  print('')

                  # This print statement prints a URL will show the user a picture of the meal
                  print('Here is a picture of the meal for reference:')
                  pprint.pprint(meal['strMealThumb'])
                  print('')

                  # Write out the recipe to a output file:
                  inputFilename = 'NoRecipe.txt'
                  # BE CAREFUL! If a file with the outputFilename name already exists,
                  # this program will overwrite that file:
                  outputFilename = 'ChosenRecipe.txt'
                  # Write out the translated messsage to the output file:
                  outputFileObj = open(outputFilename, 'w')
                  outputFileObj.write(myRecipe + '  -  ' + mealInstruction)
                  outputFileObj.close()
                  print('Additionally, your recipe has been saved to your computer as ChosenRecipe.txt')
                  print('')

                  # This last function checks that the user is satisfied with their choice of recipe
                  satisfiedChef()

        # This is to ensure the code doesn't end prematurely if the user misspells or chooses an unknown recipe
        except TypeError:
            secondChance = ''
            while secondChance != '1' and secondChance != '2':
                print('Oops! We can\'t seem to find that recipe.')
                print('''If you would like try another recipe, please press 1.
If you would like to see our recipe list, press 2.''')
                secondChance = input()
                if secondChance == '1':
                    theRecipe()
                elif secondChance == '2':
                    lostChef()


# This is the third line of the main program that calls the function pickChef, which links together the other functions.
pickChef()
