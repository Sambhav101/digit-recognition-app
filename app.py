from flask import Flask, render_template, request, redirect, url_for
import json
import numpy as np
import cv2
import re
import base64
import keras
from keras.models import load_model

# model = tf.keras.load_model('model')
app = Flask(__name__)


def reshape(img):
    # make mask of where the transparent bits are
    trans_mask = img[:, :, 3] == 0

    # replace areas of transparency with white and not transparent
    img[trans_mask] = [255, 255, 255, 255]

    # new image without alpha channel...
    new_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # resize the image to 28 by 28
    resized = cv2.resize(new_img, (28, 28), interpolation=cv2.INTER_AREA)

    # convert the resized image to grayscale
    resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # resize the image to fit input shape
    resized = resized.reshape(1, 28, 28, 1)

    # normalize our image and change value of white to 0 and black to 1
    resized = (255-resized)/255

    return resized


def predict(resized_img):

    # load model from the directory
    model = load_model("cnn/model.h5")
    result = model.predict(resized_img)
    pred = int(np.argmax(result))
    percent = round(result[0, pred]/np.sum(result) * 100, 1)
    return (pred, percent)


@ app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        byteString = request.get_data(as_text=True)
        byteString = byteString.split(",")[1]
        encoded_data = base64.b64decode(byteString)
        nparr = np.frombuffer(encoded_data, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        resized_img = reshape(img)
        result = predict(resized_img)
        return json.dumps(result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
