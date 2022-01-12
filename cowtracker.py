#!/Users/damir00/miniconda3/bin/python3

from wand.image import Image
import numpy as np
import cv2


with Image(filename='images/1280px-checkers-green-dark.png') as img:
    print(img.size)
    img.virtual_pixel = 'transparent'
    img.distort('barrel', (0.2, 0.0, 0.0, 1.0))
    img.save(filename='checks_barrel.png')
    # convert to opencv/numpy array format
    img_opencv = np.array(img)

# display result with opencv
# cv2.imshow("BARREL", img_opencv)
# cv2.waitKey(0)

# define the three background images
image_left_file = 'images/1280px-checkers-green-dark.png'
image_mid_file = 'images/1280px-checkers-green-dark.png'
image_right_file = 'images/1280px-checkers-green-dark.png'

# load the three background images
img_left = cv2.imread(image_left_file)
img_right = cv2.imread(image_right_file)

#middle pic is different - distort
image_mid = Image(filename=image_mid_file)
image_mid.virtual_pixel = 'transparent'
image_mid.distort('barrel', (0.2, 0.0, 0.0, 1.0))
image_mid.save(filename='images/barrel-distort-mid.png')

# bring back middle image as opencv
img_mid = cv2.imread('images/barrel-distort-mid.png')

# now concatenate and display as one image
img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
cv2.imshow("concatenated",img_concatenate)
cv2.waitKey(0)
cv2.destroyAllWindows()

# what are the image dimensions?
print (img_concatenate.shape)
img_width = img_concatenate.shape[1]
img_height = img_concatenate.shape[0]

def add_cow(image_name, location, cow_size):
    # location is center coordinates
    # cow_size is width and length of the cow
    # angle, angle start, angle end
    # color, in RGB truple
    # thickeness (we want it full)
    image = cv2.ellipse(image_name, location, cow_size, 0, 0, 360, (0x11, 0x11, 0x55), cow_size[1])
    return image

cow_size = (50,25)

img_with_cow = add_cow(img_concatenate, (50, 640), cow_size)
cv2.imshow("With Cow",img_with_cow)
cv2.waitKey(0)
cv2.destroyAllWindows()

def create_cow_movie(img_name, starting_location, direction, speed):
    xy = (starting_location[0], starting_location[1])
    iteration = 100
    while xy[0] < img_width:
        img_with_cow = add_cow(img_name, xy, cow_size)
        cv2.imshow("With Cow",img_with_cow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        xy = (xy[0] + speed, xy[1])

create_cow_movie(img_concatenate, (100, 640), 0, 50)
