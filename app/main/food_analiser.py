import requests
import re

class FoodAnaliser:
    def __init__(self):
        self.URL_BASE = "https://www.calorieking.com"
        self.URL_SEARCH = "/us/en/foods/search"

    # Use example:
    # fa = FoodAnaliser()
    # print(fa.get_food_nutritions("pizza"))

    def get_food_nutritions(self, foodName):
        foodUrl = self.get_food_representative(foodName)
        foodPage = self.get_food_page(foodUrl)
        return {
            "food": foodName,
            "calories": self.get_calories(foodPage),
            "fat": self.get_fat(foodPage),
            "carbs": self.get_carbs(foodPage),
            "protin": self.get_protin(foodPage),
            "fiber": self.get_fiber(foodPage)
        }

    def get_food_representative(self, foodName):
        PARAMS = {'keywords': foodName}
        r = requests.get(url = self.URL_BASE + self.URL_SEARCH, params = PARAMS)
        txt = r.text
        pattern = 'href="(\/us\/en\/foods\/f\/calories-in[a-zA-Z\/\d-]*)">'
        m = re.search(pattern, txt)
        return m.group(1)

    def get_food_page(self, foodUrl):
        r = requests.get(url = self.URL_BASE + foodUrl)
        return r.text

    def get_calories(self, foodPage):
        m = re.search('(\d*) Calories', foodPage)
        return int(m.group(1))

    def get_fat(self, foodPage):
        return self.get_ingredient('Fat', foodPage)

    def get_carbs(self, foodPage):
        return self.get_ingredient('Carbs', foodPage)

    def get_fiber(self, foodPage):
        return self.get_ingredient('Fiber', foodPage)

    def get_protin(self, foodPage):
        return self.get_ingredient('Protein', foodPage)

    def get_ingredient(self, ingredient, foodPage):
        pattern = ingredient + '</span></th><td class="MuiTableCell-root jss381 MuiTableCell-body MuiTableCell-alignCenter"><span class="MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock">([\d\.]*)'
        m = re.search(pattern, foodPage)
        result = m.group(1)
        if result == '':
            return 0
        else:
            return float(result)
