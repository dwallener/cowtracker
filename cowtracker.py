#!/Users/damir00/miniconda3/bin/python3

from wand.image import Image as WandImage
import numpy as np
import cv2


# support functions to convert between imaging libraries
#from PIL import Image, ImageFilter, ImageEnhance

def pil2cv(image_name):
     pil_image = image_name.convert('RGB')
     open_cv_image = numpy.array(pil_image)
     # this ridiculouseness flips RGB to BGR
     open_cv_image = open_cv_image[:, :, ::-1].copy()
     return open_cv_image

def cv2pil(image_name):
    cv_image = cv2.cvtColor(image_name, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(cv_image)
    return im_pil


with WandImage(filename='images/1280px-checkers-green-dark.png') as img:
    print(img.size)
    img.virtual_pixel = 'transparent'
    img.distort('barrel', (0.2, 0.0, 0.0, 1.0))
    img.save(filename='checks_barrel.png')
    # convert to opencv/numpy array format
    img_opencv = np.array(img)

# display result with opencv
# cv2.imshow("BARREL", img_opencv)
# cv2.waitKey(0)

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

# define the three background images
image_left_file = 'images/1280px-checkers-green-dark.png'
image_mid_file = 'images/1280px-checkers-green-dark.png'
image_right_file = 'images/1280px-checkers-green-dark.png'

# load the three background images
img_left = cv2.imread(image_left_file)
img_right = cv2.imread(image_right_file)

#middle pic is different - distort
image_mid = WandImage(filename=image_mid_file)
image_mid.virtual_pixel = 'black'
image_mid.distort('barrel', (0.2, 0.0, 0.0, 1.0))
image_mid.save(filename='images/barrel-distort-mid.png')

# this is used to generate the "cow in fisheye" middle frame
def distort_background(image_name):
    image_name.virtual_pixel = 'transparent'
    image_name.distort('barrel', (0.2, 0.0, 0.0, 1.0))
    image_name.save(filename='images/temp-barrel-distort.png')

# bring back middle image as opencv
img_mid = cv2.imread('images/barrel-distort-mid.png')

# now concatenate and display as one image
test_concatenation = 0
img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
pil_img_concatenate = Image.new('RGB', size=(img_concatenate.shape[0], img_concatenate.shape[1]))

if test_concatenation == 1:
    cv2.imshow("concatenated",img_concatenate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# what are the image dimensions?
print (img_concatenate.shape)
img_width = img_concatenate.shape[1]
img_height = img_concatenate.shape[0]

def add_cow_cv2(image_name, location, cow_size):
    # location is center coordinates
    # cow_size is width and length of the cow
    # angle, angle start, angle end
    # color, in RGB truple
    # thickeness (we want it full)
    starting_img = image_name
    return_image = cv2.ellipse(starting_img, location, cow_size, 0, 0, 360, (0x11, 0x11, 0x55), cow_size[1])
    return return_image

cow_size = (50,25)

test_single_cow = 0
if test_single_cow == 1:
    img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
    img_with_cow = add_cow_cv2(img_concatenate, (50, 640), cow_size)
    cv2.imshow('frame1',img_with_cow)
    cv2.waitKey(0)
    cv2.destroyWindow('frame1')

    img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
    img_with_cow2 = add_cow_cv2(img_concatenate, (100, 640), cow_size)
    cv2.imshow('frame2',img_with_cow2)
    cv2.waitKey(0)
    cv2.destroyWindow('frame2')

    img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
    img_with_cow3 = add_cow_cv2(img_concatenate, (150, 640), cow_size)
    cv2.imshow('frame3',img_with_cow3)
    cv2.waitKey(0)
    cv2.destroyWindow('frame3')

# this just moves things horizontally for now
# img_name in this usage holds the background canvas
def create_cow_movie_cv2(img_name, starting_location, direction, speed):
    xy = (starting_location[0], starting_location[1])
    iteration = 100
    while xy[0] < img_width:
        img_concatenate = np.concatenate((img_left, img_mid, img_right), axis=1)
        img_with_cow = add_cow_cv2(img_concatenate, xy, cow_size)
        cv2.imshow("Cow",img_with_cow)
        cv2.waitKey(0)
        cv2.destroyWindow("Cow")
        xy = (xy[0] + speed, xy[1])

create_cow_movie_cv2(img_concatenate, (100, 640), 0, 50)

# now let's define the field we're playing in
# three overlapping cameras covering one contiguous rectangle
# let's say the middle camera overlaps by 15% on each side
# each camera is covering a square area 1280 pixels wide
# so total field is 1280 + 1280 * .5 + 1280 -> 3200
# the concatenated images are 1280*3 -> 3840
# so now we create the coordinate mapping

# there will be a complication! because of overlap, the cow will sometimes be
# visible on both cameras at once!

def place_cow(location, cow_size):
    pass

def map_actual_coords_to_video_coords():

    overlap_width = int(1280/4)
    zone_left = (0, 1280)
    zone_left_mid = (1280-overlap_width, 1280+overlap_width)
    zone_mid = (1280+overlap_width, 1280*2 - overlap_width)
    zone_mid_right = (1280*2-overlap_width, 1280*2+overlap_width)
    zone_right = (1280*2, 1280*3)
