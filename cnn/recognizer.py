import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import keras

from keras.models import Sequential
from keras.layers import *
from keras.regularizers import l2
from keras.preprocessing.image import ImageDataGenerator


# load the dataset
mnist = tf.keras.datasets.mnist


# split the data between training set and testing set
(x_train, y_train), (x_test, y_test) = mnist.load_data()


# preprocessing data

# Normalize our image to center the values
x_train = x_train/255.0
x_test = x_test/255.0


# one hot encode the output data using to_categorical
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)


# reshape the image
img_rows, img_cols = 28, 28
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)


# data augmentation
datagen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08,
                             shear_range=0.3, height_shift_range=0.08, zoom_range=0.08)
training_generator = datagen.flow(x_train, y_train, batch_size=256)
validation_generator = datagen.flow(x_test, y_test, batch_size=256)


# design a model

# Create a convolutional neural network
model = Sequential([
    # Layer 1
    Conv2D(filters=32, kernel_size=5, strides=1, activation='relu',
           input_shape=(28, 28, 1), kernel_regularizer=l2(0.0005)),
    BatchNormalization(),
    # — — — — — — — — — — — — — — — — #
    # Layer 2
    Activation('relu'),
    MaxPooling2D(pool_size=2, strides=2),
    Dropout(0.25),
    # — — — — — — — — — — — — — — — — #
    # Layer 3
    Conv2D(filters=64, kernel_size=3, strides=1,
           activation='relu', kernel_regularizer=l2(0.0005)),
    BatchNormalization(),
    # — — — — — — — — — — — — — — — — #
    # Layer 4
    Activation('relu'),
    MaxPooling2D(pool_size=2, strides=2),
    Dropout(0.25),
    Flatten(),
    # — — — — — — — — — — — — — — — — #
    # Layer 5
    Dense(units=128, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.25),
    # — — — — — — — — — — — — — — — — #
    # Layer 6
    Dense(units=64, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.25),
    # — — — — — — — — — — — — — — — — #
    # Layer 7
    Dense(units=32, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.25),


    # Output layer
    Dense(units=10, activation='softmax')
])


# compile and fit our model
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])


early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=3, restore_best_weights=True)
history = model.fit_generator(training_generator,
                              steps_per_epoch=44100//256,
                              epochs=30,
                              validation_steps=44100//256,
                              validation_data=validation_generator,
                              callbacks=[early_stop])


# model.fit(x_train, y_train, epochs=15, batch_size= 3, verbose=1)
model.save("model.h5")


# evaluate our model to see the accuracy in test sets
model.evaluate(x_test, y_test, verbose=1)
