"""Raspberry Pi Face Recognition Treasure Box
Face Detection Helper Functions
Copyright 2013 Tony DiCola 

Functions to help with the detection and cropping of faces.
"""
import cv2
import denexapp_config as dconfig
import config




def crop(image, x, y, w, h):
    """Crop box defined by x, y (upper left corner) and w, h (width and height)
    to an image with the same aspect ratio as the face training data.  Might
    return a smaller crop if the box is near the edge of the image.
    """
    crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
    midy = y + h/2
    y1 = max(0, midy-crop_height/2)
    y2 = min(image.shape[0]-1, midy+crop_height/2)
    return image[y1:y2, x:x+w]

def resize(image):
    """Resize a face image to the proper size for training and detection.
    """
    return cv2.resize(image,
                      (config.FACE_WIDTH, config.FACE_HEIGHT),
                      interpolation=cv2.INTER_LANCZOS4)