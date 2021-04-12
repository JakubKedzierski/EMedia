import cv2 as cv
import numpy as np


def fast_fourier_transformation(image_path):
    im_data = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    f = np.fft.fft2(im_data)
    f_shifted = np.fft.fftshift(f)

    magnitude = 20 * np.log(np.abs(f_shifted))
    magnitude = 255 * magnitude / np.max(magnitude)
    magnitude = np.asarray(magnitude, dtype=np.uint8)

    phase = np.angle(f_shifted)

    cv.namedWindow('magnitude', cv.WINDOW_NORMAL)
    cv.imshow('magnitude', magnitude)

    cv.namedWindow('phase', cv.WINDOW_NORMAL)
    cv.imshow('phase', phase)
    cv.waitKey(0)


def display_image(image_path):
    im_data = cv.imread(image_path)
    cv.namedWindow('Image', cv.WINDOW_NORMAL)
    cv.imshow('Image', im_data)
    cv.waitKey(0)