import cv2
import numpy as np

# Baca gambar dan ubah ke grayscale
image = cv2.imread('Image/image6.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold biner
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Buat kernel morfologi kecil (misalnya 3x3)
kernel = np.ones((3, 3), np.uint8)

# Hilangkan titik-titik kecil dengan opening
cleaned = cv2.erode(binary, kernel, iterations=2)

# Tampilkan hasil
cv2.imshow('Tanpa Titik Kecil', cleaned)
cv2.waitKey(0)
cv2.destroyAllWindows()
