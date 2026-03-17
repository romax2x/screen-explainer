import cv2
import numpy as np


def preprocess_image(img):

    # увеличение
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # автоинверсия для тёмной темы
    if gray.mean() < 120:
        gray = cv2.bitwise_not(gray)

    # повышение контраста
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # лёгкое сглаживание
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    # бинаризация
    thresh = cv2.threshold(gray,140,255,cv2.THRESH_BINARY)[1]

    return thresh