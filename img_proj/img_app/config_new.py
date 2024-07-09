from skimage.color import rgb2lab
import numpy as np
# from skimage.color import deltaE_cie76

color_map = { 
    'Dark Red':(255,0,0),
    'Light Red':(255,102,102),
    'Dark Green':(0,102,51),
    'Light Green':(51,255,51),
    'Dark Blue':(0,0,204),
    'Light Blue':(51,153,255),
    'Light Yellow':(255,255,204),
    'Dark Yellow':(255,255,0),
    'Golden':(255,215,0),
    'Black':(0,0,0),
    'White':(255,255,255),
    #'Silver':(192,192,192),
    'Orange':(255,128,0),
    'Pink':(255,0,255),
    'Purple':(128,0,128),
    'Grey':(224,224,224),
    'Light Brown':(153,76,0),
    'Dark Brown': (102,0,0),
    'Maroon':(128,0,0),
    'Cyan':(0,255,255),
    'Magenta':(255,0,0),
    'Teal':(0,153,153),
    'Skin':(255,204,153),
    'Cream':(255,229,204),
    'Light Orange':(255,178,102),
    'Parrot Green':(0,153,0)
}


# def convert_rgb_to_lab(color):
    
#     return rgb2lab(np.array(np.ones((1, 1, 3)) * color/255))

# color_map_lab = {}
# for key, val in color_map.items():
#     # val = convert_rgb_to_lab(val)
#     color_map_lab[key] = rgb2lab(np.array(np.ones((1, 1, 3)) * val/255))


# def cie76(c1, c2):
#     return np.linalg.norm(np.array(c1)-np.array(c2))
    #return deltaE_cie76(c1,c2)

# for key, val in color_map_lab.items():
#     print(f"'{key}':{val}")