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
                check_clr = {}
                color = []
                if img_obj.mode=='L':
                    return render(req, 'color_info.html',{'form':form,'msg':"The image is Grayscale."})
                for clr in img_colors:
                    color.append(tuple(close_color(clr[:3])))
                colors = defaultdict(int)
                
                for clr in color :
                    colors[clr]+=1
                colors = dict(sorted(colors.items(), key = lambda item: item[1], reverse=True))
                
            
               
                colors = dict(list(colors.items()))
                color_dict = {}
                
                for clr, cnt in Counter(colors).items():
                    
                    if clr in color_green_list:
                        clr = color_green
                    elif clr in color_yellow_list:
                        clr = color_yellow
                    elif clr in color_blue_list:
                        clr = color_blue
                    elif clr in color_purple_list:
                        clr = color_purple
                    elif clr in color_red_list:
                        clr = color_red
                    elif clr in color_black_list:
                        clr = color_black 
                    elif clr in color_orange_list:
                        clr = color_orange
                    elif clr in color_white_list:
                        clr = color_white
                    color_dict[clr] = cnt

                total = sum(Counter(color_dict).values())
                k = min(len(color_dict), int(k))
                for clr, cnt in Counter(color_dict).items():
                    print(f"cnt: {cnt}, total: {total}, perc: {round((cnt/total)*100, 4)}")
                    color_dict[clr] = round((cnt/total)*100, 4)
                    
                color_dict = {get_color(clr):val for clr, val in colors.items()}
                # color_dict = dict(sorted(color_dict.items(), key = lambda item: item[1], reverse=True))
                color_dict = dict(list(color_dict.items())[:k])
                color_dict = dict(sorted(color_dict.items(), key = lambda item: item[1], reverse=True))
                
                for clr, cnt in Counter(color_dict).items():
                    print(f"cnt: {cnt}, total: {total}, perc: {round((cnt/total)*100, 4)}")
                    print(f"color: {clr}: {color_dict[clr]}\n")
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
    #color= colorsys.rgb_to_hsv(color[0], color[1], color[2])
    color = rgb2lab(color)
    color = np.array(color)
    #dist = np.sqrt(np.sum((colors_list_lab -color)**2, axis = 1))
    dist = deltaE_cie76(color, colors_list_lab)
    color_keys = list(color_pallette.keys())
    return color_keys[np.argmin(dist)]

def extract_top_colors(req):
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
                
                img_colors = list(img_obj.getdata())
                
                color = []
                if img_obj.mode=='L':
                    return render(req, 'color_info.html',{'form':form,'msg':"The image is Grayscale."})
                
                for clr in img_colors:
                    color.append(tuple(find_neareat_color(clr[:3])))
                colors = defaultdict(int)
                
                for clr in color :
                    colors[clr]+=1
                colors = dict(sorted(colors.items(), key = lambda item: item[1], reverse=True))
                #colors = dict(list(colors.items()))
                
                color_dict = {}
                for clr, cnt in Counter(colors).items():
                    
                    if clr in color_green_list:
                        clr = color_green
                    elif clr in color_yellow_list:
                        clr = color_yellow
                        
                    elif clr in color_blue_list:
                        clr = color_blue
                    elif clr in color_purple_list:
                        clr = color_purple
                    elif clr in color_red_list:
                        clr = color_red
                    elif clr in color_black_list:
                        clr = color_black 
                    elif clr in color_orange_list:
                        
                        clr = color_orange
                    elif clr in color_white_list:
                        clr = color_white    
                    color_dict[clr] = cnt
                
                total = sum(Counter(color_dict).values())
                k = min(len(color_dict), int(k))
                for clr, cnt in Counter(color_dict).items():
                    color_dict[clr] = round((cnt/total)*100, 4)
                    
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

