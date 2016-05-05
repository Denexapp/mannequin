"""Raspberry Pi Face Recognition Treasure Box 
Pi Camera OpenCV Capture Device
Copyright 2013 Tony DiCola 

Pi camera device capture class for OpenCV.  This class allows you to capture a
single image from the pi camera as an OpenCV image.
"""
import io
import time
import file_io

import cv2
import numpy as np
import picamera

import config


class OpenCVCapture(object):
	def read(self):
		"""Read a single frame from the camera and return the data as an OpenCV
		image (which is a numpy array).
		"""
		# This code is based on the picamera example at:
		# http://picamera.readthedocs.org/en/release-1.0/recipes1.html#capturing-to-an-opencv-object
		# Capture a frame from the camera
		print "debug_picam_0"
		data = io.BytesIO()
		print "debug_picam_1"
		#
		# try:
		# 	picamera.PiCamera().capture(data, format='jpeg')
		# except BaseException as e:
		# 	print e.message, e.args, e, str(e)
		# 	file_io.write("camera_error.txt", e.message + "\n" + str(e.args) + "\n" + str(e) + "\n" + str(e))
		with picamera.PiCamera() as camera:
			print "debug_picam_2"
			camera.capture(data, format='jpeg')
		print "debug_picam_3"
		data = np.fromstring(data.getvalue(), dtype=np.uint8)
		print "debug_picam_4"
		# Decode the image data and return an OpenCV image.
		image = cv2.imdecode(data, 1)
		print "debug_picam_5"
		# Save captured image for debugging.
		cv2.imwrite(config.DEBUG_IMAGE, image)
		# Return the captured image data.
		return image
