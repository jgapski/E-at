from flask import Flask
import cv2
import os
from food_classifier import FoodClassifier
from food_analiser import FoodAnaliser

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/food_prediction')
def predict_food():
    image = cv2.imread("C:/Users/Efe/Documents/GitHub/E-at/app/test_images/salad_test.jpg")   ## this is a placeholder hardcode
    food_clf = FoodClassifier()
    prediction = food_clf.predict(image)

    fa = FoodAnaliser()
    return fa.get_food_nutritions(prediction)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
