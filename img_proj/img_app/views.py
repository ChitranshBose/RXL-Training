from itertools import count
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from img_app.models import Upload
from .forms import UploadImage
from PIL import Image
from collections import Counter
from .color_config import *
from .color_config_lab import *
import numpy as np
from sklearn.cluster import kmeans_plusplus, KMeans
from collections import defaultdict
from colormath.color_objects import LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import colorsys
from .configuration import *
# Create your views here.
def upload_img_info(req):
    if req.method == "POST":
        form = UploadImage(req.POST, req.FILES)
        if form.is_valid():
            save = form.save()
            image = form.instance
            img_path = os.path.join(settings.MEDIA_ROOT, str(save.img))
            with Image.open(img_path) as img_obj:
                w, h = img_obj.size
                img_format = img_obj.format
                type = img_obj.mode
                if type == 'L':
                    type = 'Grayscale'
                size_bytes = os.path.getsize(img_path)
                size_kb = round(size_bytes/1024, 2)
                context = {
                    'form': form,
                    'width': w,
                    'height': h,
                    'img_format': img_format,
                    'img_type': type,
                    'size_bytes': size_bytes,
                    'size_kb': size_kb,
                    'image': image
                }
           
                
            return render(req, 'input.html',context)
    else:
        form = UploadImage()
    images = Upload.objects.all()
    return render(req, 'input.html',{"images":images,'form':form})

def close_color(color):
    colors = np.array(colors_list)
    color = np.array(color)
    dist = np.sqrt(np.sum((colors-color)**2, axis = 1))
    color_keys = list(color_pallette.keys())
    return color_keys[np.argmin(dist)]

def get_color(color):
    return 'rgb({},{},{})'.format(*color)

def fetch_top_colors(req):
    global img_file, img_instance
    if req.method == "POST":
        form = UploadImage(req.POST, req.FILES)
        if form.is_valid():
            if 'img' in req.FILES:
                save = form.save()
                img_instance = form.instance
                img_file = os.path.join(settings.MEDIA_ROOT, str(save.img))
            # save = form.save()
            image = img_instance
            k = req.POST['drop_down']
            #img_path = os.path.join(settings.MEDIA_ROOT, str(save.img))
            img_path = img_file
            with Image.open(img_path) as img_obj:
                
                img_colors = list(img_obj.getdata())
                # check_clr = {}
                color = []
                if img_obj.mode=='L':
                    return render(req, 'color_info.html',{'form':form,'msg':"The image is Grayscale."})
                
                for clr in img_colors:
                    color.append(tuple(close_color(clr[:3])))
                colors = defaultdict(int)
                
                for clr in color :
                    colors[clr]+=1
                colors = dict(sorted(colors.items(), key = lambda item: item[1], reverse=True))
                color_dict = {}
                for clr, cnt in Counter(colors).items():
                    if clr in color_dict:
                        
                        color_dict[clr] += cnt
                    else:
                        
                        color_dict[clr] = cnt
               
                colors = dict(list(color_dict.items()))
                # color_dict = {}
                total = sum(Counter(color_dict).values())
                for clr, cnt in Counter(color_dict).items():
                    
                    print(f"COLOR: {clr}\n")
                    if clr == (51, 255, 153):
                        print("cb\n")
                    if clr in color_green_list:
                        print(f"green: {clr}\n")
                        clr = color_green
                    elif clr in color_yellow_list:
                        #print(f"yellow: {clr}\n")
                        clr = color_yellow
                    elif clr in color_blue_list:
                        #print(f"blue: {clr}\n")
                        clr = color_blue
                    elif clr in color_purple_list:
                        #print(f"purple: {clr}\n")
                        clr = color_purple
                    elif clr in color_red_list:
                        #print(f"red: {clr}\n")
                        clr = color_red
                    elif clr in color_black_list:
                       # print(f"clack: {clr}\n")
                        clr = color_black 
                    elif clr in color_orange_list:
                        #print(f"orange: {clr}\n")
                        clr = color_orange
                    elif clr in color_white_list:
                        #print(f"white: {clr}\n")
                        clr = color_white
                    else:
                        print(f"other: {clr}\n")
                    #if clr in color_dict:
                    color_dict[clr] = round((cnt/total)*100, 4)

                # total = sum(Counter(color_dict).values())
                k = min(len(color_dict), int(k))
                # for clr, cnt in Counter(color_dict).items():
                #     #print(f"cnt: {cnt}, total: {total}, perc: {round((cnt/total)*100, 4)}")
                #     color_dict[clr] = round((cnt/total)*100, 4)
                    
                color_dict = {get_color(clr):val for clr, val in color_dict.items()}
                color_dict = dict(sorted(color_dict.items(), key = lambda item: item[1], reverse=True))
                color_dict = dict(list(color_dict.items())[:k])
                
            
                context = {
                    'form': form,
                    'image': image,
                    'top_colors': color_dict
                }

                
            return render(req, 'color_info.html',context)
    else:
        form = UploadImage()
    images = Upload.objects.all()
    return render(req, 'color_info.html',{"images":images,'form':form})

def find_neareat_color(color):
    clr = color
    color= colorsys.rgb_to_hsv(color[0], color[1], color[2])
    #print(f"color before: {color}\n")
    #color = rgb2lab(color)
    #print(f"color: after {color}\n")
    color = np.array(color)
    
    dist = np.sqrt(np.sum((colors_list_val - color)**2, axis = 1))
    #dist = deltaE_cie76(color, colors_list_val)
    # color_keys = list(color_pallette.keys())
    # print(f"dist: {np.argmin(dist)}\n")
    return colors_list_key[np.argmin(dist)]

def extract_top_colors(req):
    global img_file, img_instance
    if req.method == "POST":#
        form = UploadImage(req.POST, req.FILES)
        if form.is_valid():
            if 'img' in req.FILES:
                save = form.save()
                img_instance = form.instance
                img_file = os.path.join(settings.MEDIA_ROOT, str(save.img))
            image = img_instance
            k = req.POST['drop_down']
            img_path = img_file
            with Image.open(img_path) as img_obj:
                
                img_colors = list(img_obj.getdata())
                
                color = []
                if img_obj.mode=='L':
                    return render(req, 'color_info.html',{'form':form,'msg':"The image is Grayscale."})
                # print(f"color list lab : {colors_list_lab}\n")
                for clr in img_colors:
                    print(f"value: {find_neareat_color(clr[:3])}")
                    color.append(tuple(find_neareat_color(clr[:3])))
                colors = defaultdict(int)
                
                for clr in color :
                    colors[clr]+=1
                colors = dict(sorted(colors.items(), key = lambda item: item[1], reverse=True))
                #colors = dict(list(colors.items()))
                map = {}
                color_dict = {}
                # print(f"colors: {colors}\n")
                for clr, cnt in Counter(colors).items():
                    #print(f"color :{clr}\n")
                    if clr in color_green_list:
                        clr = color_green
                        map[clr] = "green"
                        # print(f"color :{clr}\n")
                    elif clr in color_yellow_list:
                        clr = color_yellow
                        map[clr] = "yellow"
                    elif clr in color_blue_list:
                        clr = color_blue
                        map[clr] = "blue"
                    elif clr in color_purple_list:
                        clr = color_purple
                        map[clr] = "purple"
                    elif clr in color_red_list:
                        clr = color_red
                        map[clr] = "red"
                    elif clr in color_black_list:
                        clr = color_black
                        map[clr] = "black" 
                    elif clr in color_orange_list:
                        map[clr] = "orange"
                        clr = color_orange
                    elif clr in color_white_list:
                        clr = color_white    
                        map[clr] = "white"
                    map[clr] = "other"
                    color_dict[clr] = cnt
                #print(f"map: {map}\n")
                total = sum(Counter(color_dict).values())
                k = min(len(color_dict), int(k))
                for clr, cnt in Counter(color_dict).items():
                    color_dict[clr] = round((cnt/total)*100, 4)
                ## hsv to rgb
                for clr in color_dict:
                    clr = colorsys.hsv_to_rgb(clr[0], clr[1], clr[2])
                color_dict = {get_color(clr):val for clr, val in color_dict.items()}
                color_dict = dict(sorted(color_dict.items(), key = lambda item: item[1], reverse=True))
                color_dict = dict(list(color_dict.items())[:k])
                
                context = {
                    'form': form,
                    'image': image,
                    'top_colors': color_dict
                }

                
            return render(req, 'color_info.html',context)
    else:
        form = UploadImage()
    images = Upload.objects.all()
    return render(req, 'color_info.html',{"images":images,'form':form})


def get_shade_count(color_key, color, count_map, shade_map):

    shades = color_shades[color_key]
    shades = np.array(shades)
    color = np.array(color)
    dist = np.argmin(np.sqrt(np.sum((shades - color)**2, axis = 1))) 
    shade_map[np.argmin(dist)]+=1
    count_map[color_key] = dict(shade_map)
    return count_map

def get_nearest_color(color):

    color = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    color = np.array(color)
    min_dist = float('inf')
    close_clr = None
    for clr, shades in color_shades.items():
        shades = np.array(shades)
        dist =  np.argmin(np.sqrt(np.sum((shades - color)**2, axis = 1)))
        if dist<min_dist:
            min_dist = dist
            close_clr = clr
    return close_clr

def get_shades(color, count_map):
    color = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    color = np.array(color)
    for clr, shades in color_shades.items():
        shades = np.array(shades)
        dist =  np.argmin(np.sqrt(np.sum((shades - color)**2, axis = 1)))
        count_map[clr][dist]+=1
        
    return count_map

def convert_hsv_to_rgb(color):
    rgb = tuple(np.array(colorsys.hsv_to_rgb(color[0],  color[1],  color[2])).astype('int64'))
    return rgb

def get_color_shades(req):
    global img_file, img_instance
    if req.method == "POST":
        form = UploadImage(req.POST, req.FILES)
        if form.is_valid():
            if 'img' in req.FILES:
                save = form.save()
                img_instance = form.instance
                img_file = os.path.join(settings.MEDIA_ROOT, str(save.img))
            image = img_instance
            k = req.POST['drop_down']
            img_path = img_file
            with Image.open(img_path) as img_obj:
                print("Inside image\n")
                img_colors = list(img_obj.getdata())
                
                color = []
                if img_obj.mode=='L':
                    return render(req, 'show_color_shades.html',{'form':form,'msg':"The image is Grayscale."})
                count_map = defaultdict(int)
                for key, val in color_shades.items():
                    count_map[key] = [0]*(len(val))
                
                for clr in img_colors:
                    clr = clr[:3]
                    count_map = get_shades(clr, count_map)
                total = 0
                for key,val in count_map.items():
                    total+=sum(val)
                
                for key,val in count_map.items():
                    val = list(np.round((np.array(val)/total)*100,4))
                    count_map[key]=val
                
                
                for clr, shades in color_shades.items():
                    color_shades[clr] = [convert_hsv_to_rgb(shade) for shade in shades]
                color_dict = {}
                for key in color_shades:
                    rgb_lst = color_shades[key]
                    perc_lst = count_map[key]
                    rgb_lst = [get_color(clr) for clr in rgb_lst]
                    lst = [(rgb, perc) for rgb, perc in zip(rgb_lst, perc_lst)]
                    color_dict[key] = lst
                
                

                k = min(len(count_map), int(k))
                color_dict = dict(list(color_dict.items())[:k])
                print(f"color_dict: {color_dict}\n")
                context = {
                    'form': form,
                    'image': image,
                    'top_colors': color_dict
                }
            return render(req, 'show_color_shades.html',context)
    else:
        form = UploadImage()
    images = Upload.objects.all()
    return render(req, 'show_color_shades.html',{"images":images,'form':form})
