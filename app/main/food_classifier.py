import cv2
from keras.models import load_model

class FoodClassifier():
    def __init__(self):
        self.model = load_model("../tensorflow_models/food_detector_model.h5")

    def decode_prediction(self, class_id):
        class_dict = {
            0: "pasta",
            1: "donut",
            2: "fries",
            3: "apple",
            4: "pizza",
            5: "salad"
        }

        return class_dict[class_id]

    def predict(self, image):
        image = image[..., ::-1]
        image = cv2.resize(image, (200, 200))
        image = image.reshape(-1, 200, 200, 3)

        encoded_prediction = int(self.model.predict_classes(image))
        return self.decode_prediction(encoded_prediction)