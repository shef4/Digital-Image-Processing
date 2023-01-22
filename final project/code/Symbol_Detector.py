#class to build and train a symbol detector for 
# right side up triangles, upside down triangle, squares, circles, and 
# an arrow pointng to the right using CNNs

import numpy as np
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import model_from_json

class Symbol_Detector:
    def __init__(self):
        self.categories = ["circle","down_triangle", "square", "up_triangle"]
        self.model = None
    
    def load_model(self):
        json_file = open('data/model/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("data/model/model.h5")
        self.model = loaded_model


    def predict(self, img):
        #empty numpy image of shape img.shape
        pred_img = np.zeros(img.shape)
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                pred_img[row][col] = img[row][col][1]

        # resize image to 50x50
        pred_img = cv2.resize(pred_img, (50, 50))

        # predict
        prediction = self.model.predict(pred_img.reshape(1, 50, 50, 1)) 
        return prediction[0],self.categories[np.argmax(prediction[0])]