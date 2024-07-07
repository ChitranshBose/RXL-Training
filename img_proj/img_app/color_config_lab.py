from colormath.color_objects import sRGBColor,  LabColor
from colormath.color_conversions import convert_color
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76
import colorsys

colors_list_tup = [
    [255, 0, 0], 
    [0, 0, 255], 
    [0, 255, 0], 
    [255, 255, 0], 
    [255, 255, 255], 
    [0, 0, 0], 
    [153, 76, 0], 
    [255, 128, 0], 
    [153, 0, 153], 
    [255, 0, 255], 
    [255, 255, 102], 
    [0, 0, 102], 
    [0, 153, 0], 
    [51, 255, 255], 
    [127, 0, 255], 
    [153, 153, 0], 
    [51, 255, 153], 
    [51, 0, 51], 
    [204, 0, 0], 
    [255, 51, 51], 
    [51, 153, 255], 
    [255, 255, 204], 
    [0, 244, 244], 
    #[160, 160, 160], 
    [204, 204, 204], 
    [0, 0, 51], 
    [0, 25, 51], 
    [153, 0, 0], 
    [32, 32, 32], 
    [128, 0, 0], 
    [139, 0, 0], 
    [165, 42, 42], 
    [178, 34, 34], 
    [220, 20, 60], 
    [255, 99, 71], 
    [255, 127, 80], 
    [205, 92, 92], 
    [240, 128, 128], 
    [233, 150, 122], 
    [250, 128, 114], 
    [255, 160, 122], 
    [255, 69, 0], 
    [255, 69, 0], 
    [255, 140, 0], 
    [255, 165, 0], 
    [154, 205, 50], 
    [85, 107, 47], 
    [107, 142, 35], 
    [124, 252, 0], 
    [127, 255, 0], 
    [173, 255, 47], 
    [0, 100, 0], 
    [0, 128, 0], 
    [34, 139, 34], 
    [50, 205, 50], 
    [144, 238, 144], 
    [152, 251, 152], 
    [143, 188, 143], 
    [0, 250, 154], 
    [0, 255, 127], 
    [46, 139, 87], 
    [102, 205, 170], 
    [60, 179, 113], 
    [32, 178, 170], 
    [47, 79, 79], 
    [0, 128, 128], 
    [0, 139, 139], 
    [70, 130, 180], 
    [100, 149, 237], 
    [0, 191, 255], 
    [30, 144, 255], 
    [173, 216, 230], 
    [135, 206, 235], 
    [135, 206, 250], 
    [25, 25, 112], 
    [0, 0, 128], 
    [0, 0, 139], 
    [0, 0, 205], 
    [65, 105, 225], 
    [138, 43, 226], 
    [75, 0, 130], 
    [72, 61, 139], 
    [64, 64, 64], 
    [96, 96, 96], 
    [51, 102, 153], 
    [19, 72, 139], 
    [0, 51, 102], 
    [51, 51, 153], 
    # [84, 55, 111], 
    [102, 255, 153], 
    [51, 255, 102], 
    [51, 51, 102], 
    [102, 102, 153], 
    [51, 153, 153], 
    [255, 51, 0], 
    [0, 255, 255], 
    [102, 0, 102]
]
# color_hsv = []
colors_list_key = []
for clr in colors_list_tup:
    hsv = colorsys.rgb_to_hsv(clr[0],  clr[1],  clr[2])
    #clr_lab = rgb2lab(clr)
    #color_hsv.append(hsv)
    colors_list_key.append(hsv)

colors_list_val = np.array(colors_list_key)
def convert_rgb_to_hsv(color_list, color_repr):
    color_list_out = []
    for clr in color_list:
        hsv = colorsys.rgb_to_hsv(clr[0],  clr[1],  clr[2])
        colors_list_key.append(hsv)
    color_repr = colorsys.rgb_to_hsv(color_repr[0],  color_repr[1],  color_repr[2])
    return colors_list_key, color_repr

color_green_list = [(0,255,0),(0,153,0),(0, 244, 244),(51,255,153)]
color_yellow_list = [(255,255,0),(255,255,102)]
color_blue_list = [(0,0,255),(0,0,102),(51,153,255)]
color_purple_list = [(102,0,102),(51,0,51),(153,0,153)]
color_red_list = [(255,0,0),(204,0,0),(255,51,51)]
color_black_list = [(0,0,0),(0,0,51),(0,25,51)]
color_white_list = [(255,255,255)]
color_orange_list = [(255,128,0)]

color_green = (0,255,0)
color_yellow = (255,255,0)
color_blue = (0,0,255)
color_purple = (102,0,102)
color_red = (255,0,0)
color_black = (0,0,0)
color_white = (255,255,255)
color_orange = (255,128,0)

color_green_list, color_green = convert_rgb_to_hsv(color_green_list, color_green)
color_yellow_list, color_yellow = convert_rgb_to_hsv(color_yellow_list, color_yellow)
color_blue_list, color_blue = convert_rgb_to_hsv(color_blue_list, color_blue)
color_purple_list, color_purple = convert_rgb_to_hsv(color_purple_list, color_purple)

color_red_list, color_red = convert_rgb_to_hsv(color_red_list, color_red)
color_black_list, color_black = convert_rgb_to_hsv(color_black_list, color_black)
color_white_list, color_white = convert_rgb_to_hsv(color_white_list, color_white)
color_orange_list, color_orange = convert_rgb_to_hsv(color_orange_list, color_orange)
#print(f"color_green_list: {color_green_list}\n")