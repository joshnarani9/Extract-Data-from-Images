import cv2
import numpy as np

## (1) Convert to gray, and threshold
image_filename ='01048818.jpeg'
img = cv2.imread('Receipts/{}'.format(image_filename))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

## (2) Morph-op to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

## (3) Find the max-area contour
cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnt = sorted(cnts, key=cv2.contourArea)[-1]

## (4) Crop and save it
x,y,w,h = cv2.boundingRect(cnt)
dst = img[y:y+h, x:x+w]
cv2.imwrite("001.png", dst)
filename='Receipts/01048818.jpeg'

img = cv2.imread(filename)

#Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#Separate the background from the foreground
bit = cv2.bitwise_not(gray)
#Apply adaptive mean thresholding
amtImage = cv2.adaptiveThreshold(bit, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 15)
#Apply erosion to fill the gaps
kernel = np.ones((15,15),np.uint8)
erosion = cv2.erode(amtImage,kernel,iterations = 2)
#Take the height and width of the image
(height, width) = img.shape[0:2]
#Ignore the limits/extremities of the document (sometimes are black, so they distract the algorithm)
image = erosion[50:height - 50, 50: width - 50]
(nheight, nwidth) = image.shape[0:2]
#Create a list to save the indexes of lines containing more than 20% of black.
index = []
for x in range (0, nheight):
    line = []

    for y in range(0, nwidth):
        line2 = []
        if (image[x, y] < 150):
            line.append(image[x, y])
    if (len(line) / nwidth > 0.2):  
        index.append(x)
#Create a list to save the indexes of columns containing more than 15% of black.
index2 = []
for a in range(0, nwidth):
    line2 = []
    for b in range(0, nheight):
        if image[b, a] < 150:
            line2.append(image[b, a])
    if (len(line2) / nheight > 0.15):
        index2.append(a)

#Crop the original image according to the max and min of black lines and columns.
img = img[min(index):max(index) + min(250, (height - max(index))* 10 // 11) , max(0, min(index2)): max(index2) + min(250, (width - max(index2)) * 10 // 11)]
#Save the image
cv2.imwrite('images/new-{}'.format(filename), img)


####

from PIL import Image
#from PIL import ImageCms
import numpy
# force opening truncated/corrupt image files
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#img = "shoes.jpg"
img='Receipts/{}'.format(image_filename)
img = Image.open(img)
# =============================================================================
# if img.mode == "CMYK":
#     # color profiles can be found at C:\Program Files (x86)\Common Files\Adobe\Color\Profiles\Recommended
#     img = ImageCms.profileToProfile(img, "USWebCoatedSWOP.icc", "sRGB_Color_Space_Profile.icm", outputMode="RGB")
# =============================================================================
# PIL image -> OpenCV image; see https://stackoverflow.com/q/14134892/2202732
img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)

## (1) Convert to gray, and threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

## (2) Morph-op to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

## (3) Find the max-area contour
cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnt = sorted(cnts, key=cv2.contourArea)[-1]

## (4) Crop and save it
x,y,w,h = cv2.boundingRect(cnt)
dst = img[y:y+h, x:x+w]

# add border/padding around the cropped image
# dst = cv2.copyMakeBorder(dst, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255,255,255])

cv2.imshow("image", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# create/write to file
# cv2.imwrite("001.png", dst)