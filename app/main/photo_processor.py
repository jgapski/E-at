from food_classifier import FoodClassifier
from food_analiser import FoodAnaliser
from datetime import datetime


class PhotoProcessor:

    def __init__(self, statistics_repo):
        self.statistics_repo = statistics_repo

    def main_alg(self, username, photo):
        food_clf = FoodClassifier()
        prediction = food_clf.predict(photo)
        details = FoodAnaliser().get_food_nutritions(prediction)

        self.statistics_repo.put_statistics(username, datetime.timestamp(datetime.now()), details)

        print(username)
        print(details)
        pass
