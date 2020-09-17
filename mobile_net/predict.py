import tensorflow as tf
import numpy as np
import cv2
import os

import pickle
CLASSES = pickle.load( open("mapping","rb"))
print(CLASSES)


'''
Predicts the car type using keras model
'''
class PredictCarsData():
    
    def __init__(self):
        self.model = tf.keras.models.load_model("carspredict")
       
    def predict(self , images):
        data = np.argmax(self.model.predict(images), axis=1)
        ret_list = list()
        for r in data:
            ret_list.append(list(CLASSES.keys())[list(CLASSES.values()).index(r)])
        
        return " ,".join(ret_list)




