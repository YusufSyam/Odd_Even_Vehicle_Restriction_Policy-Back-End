import cv2
import numpy as np

def straightening_image(image):
    # Temukan tepi gambar
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Temukan garis-garis menggunakan transformasi Hough
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    # plt.imshow(edges)
    # print('/nLines/n', lines)

    if lines is None:
        return image, False

    # Temukan sudut rotasi
    for line in lines:
        rho, theta = line[0]
        if np.degrees(theta) > 45 and np.degrees(theta) < 135:
            rotation_angle = np.degrees(theta) - 90
            break
    else:
        return image, False

    # Rotasi gambar
    rows, cols = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
    rotated_img = cv2.warpAffine(image, M, (cols, rows))

    return rotated_img, True

def stretch_vertical(img, height_multiply= 1.5):
    # Dapatkan dimensi asli gambar
    height= img.shape[0]
    width = img.shape[1]
    # height, width, _ = img.shape

    # Lakukan pengstretchan secara vertikal
    stretched_height = int(height * height_multiply)
    stretched_img = cv2.resize(img, (width, stretched_height))

    # Tampilkan gambar menggunakan pyplot
    # plt.imshow(cv2.cvtColor(stretched_img, cv2.COLOR_BGR2RGB))
    # plt.title('Gambar Stretched Vertikal')
    # plt.axis('off')
    # plt.show()
    return stretched_img

def upscale_image(img, amount= 10):
    # Dapatkan dimensi asli gambar
    height, width = img.shape

    # Upscale gambar sebanyak 2x panjang dan lebar
    new_height = height *amount
    new_width = width *amount
    upscaled_img = cv2.resize(img, (new_width, new_height))

    # Simpan gambar yang sudah diupscale
    # cv2.imwrite(output_path, upscaled_img)

    return upscaled_img

def preprocess_plate(image, show= False):
    th, threshed = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # threshed = thresholding3(image)
    final_img= cv2.bitwise_not(threshed)

    if show:
        plt.imshow(final_img, cmap='binary')
        plt.show()

    return final_img

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.GaussianBlur(image, (3, 3), 0)

#thresholding1
def thresholding1(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#thresholding2
def thresholding2(image):
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

#thresholding3
def thresholding3(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 45, 15)

#dilation
def dilate(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image, kernel_size= (3,3)):
    kernel = np.ones(kernel_size,np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(9 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)