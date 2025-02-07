import cv2
from joblib import load
import glob
import numpy as np

clf = load("smile.z")

def load_pic(item):
    img = cv2.imread(item)
    img_r = cv2.resize(img,(32,32))
    img_r = img_r / 255
    img_r = img_r.flatten()
    img_r = np.array([img_r])

    label = clf.predict(img_r)[0]
    return label