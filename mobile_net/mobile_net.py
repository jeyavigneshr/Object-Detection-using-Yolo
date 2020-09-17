import tensorflow as tf
import numpy as np 
from glob import glob
import os

from PIL import Image
from datetime import datetime
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import pickle

'''
**********************************************************
Base model from Tensorflow website
**********************************************************
'''
IMG_SIZE = 224
IMG_SHAPE = (IMG_SIZE , IMG_SIZE , 3)

BATCH_SIZE = 10
IMG_HEIGHT = 224
IMG_WIDTH = 224
image_count = 1110
STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)

def resize_img(image):
    print(image)
    img = Image.open(image)
    img = img.resize((256,256) , Image.ANTIALIAS)

    img.save(image)

def format_example(image, label):
  image = tf.cast(image, tf.float32)
  image = (image/127.5) - 1
  image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
  return image, label




image_generator = tf.keras.preprocessing.image.ImageDataGenerator(validation_split=0.2,preprocessing_function=preprocess_input)

CLASS_NAMES = ["sedan", "hatchback"]
# data_dir = glob("**/*.jpg",recursive=True)
# print(data_dir)

data_dir = "data"

X_train = image_generator.flow_from_directory(directory=str(data_dir),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                    #  classes = list(CLASS_NAMES),
                                                      subset="training",
                                                      class_mode='categorical')
label = (X_train.class_indices)
print(label)
X_test = image_generator.flow_from_directory(directory=str(data_dir),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                    #  classes = list(CLASS_NAMES),
                                                     class_mode='categorical',
                                                     subset="validation")

label_t = (X_test.class_indices)
print(label_t)


pickle.dump(label,open("mapping","wb"))

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)


logdir = "logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

# Create the base model from the pre-trained model MobileNet V2

base_model = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=IMG_SHAPE)

x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dense(1280, activation='relu',  kernel_initializer= tf.keras.initializers.glorot_uniform(42), bias_initializer='zeros')(x)
x = tf.keras.layers.BatchNormalization()(x)
predictions = tf.keras.layers.Dense(2, activation='softmax', kernel_initializer='random_uniform', bias_initializer='zeros')(x)

model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

base_learning_rate = 0.0001
optimizer = tf.keras.optimizers.Adam(lr=base_learning_rate)

loss = "categorical_crossentropy"

for layer in model.layers:
    layer.trainable = True


model.summary()

model.compile(
              optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy'])



initial_epochs = 10
validation_steps=20

# loss0,accuracy0 = model.evaluate(validation_batches, steps = validation_steps)

history = model.fit(X_train,
                    epochs=initial_epochs,
                    # validation_split=0.2,
                    validation_data=X_test,
                    callbacks=[tensorboard_callback])



acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

model.save('carsdetect')
