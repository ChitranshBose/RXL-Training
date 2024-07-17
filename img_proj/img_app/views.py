
import os
from django.conf import settings

from django.shortcuts import render
from img_app.models import Upload
from .forms import UploadImage
from PIL import Image, ImageColor

import numpy as np

from collections import defaultdict

from .config_new import *
import time as t
from .config_new_map import *
import cv2  

# from pyciede2000 import ciede2000
from scipy.spatial.distance import cdist
from functools import lru_cache
from collections import Counter

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

def get_color(color):
    return 'rgb({},{},{})'.format(*color)


def mul(a,b):
    ans = 0
    while b!=0:
        if b&1:
            ans+=a
        a<<=1
        b>>=1
    return ans

def rgb_to_lab(color):
   
    num = 0
    rgb = [0,0,0]
    for clr in color:
        clr = float(clr)/255
        if clr > 0.04045:
            clr = ((clr + 0.055)/1.055)**2.4
        else:
            clr/=12.92
        rgb[num] = clr*100
        num+=1
    xyz = [0,0,0]
    x  = rgb[0]*0.4124 + rgb[1]*0.3576 +rgb[2]*0.1805
    y  = rgb[0]*0.2126 + rgb[1]*0.7152 +rgb[2]*0.0722
    z  = rgb[0]*0.0193 + rgb[1]*0.1192 +rgb[2]*0.9505
    

    xyz[0] = round(x,4)
    xyz[1] = round(y,4)
    xyz[2] = round(z,4)

    xyz[0] = float(xyz[0])/95.047
    xyz[1] = float(xyz[1])/100.0
    xyz[2] = float(xyz[2])/108.883
    num = 0
    for clr in xyz:
        if clr>0.008856:
            clr = clr**(0.3333333333333333)
        else:
            clr = (7.787*clr) + (16/116)
        xyz[num] = clr
        num+=1
    lab = [0,0,0]
    l = (116*xyz[1])-16
    a = 500*(xyz[0]-xyz[1])
    b = 200*(xyz[1]-xyz[2])
    lab[0] = round(l,4)
    lab[1] = round(a,4)
    lab[2] = round(b,4)

    
    return lab

# def fetch_colors(req):
#     st = t.time()
#     global img_file, img_instance
    
#     if req.method == "POST":
#         form = UploadImage(req.POST, req.FILES)
#         if form.is_valid():
#             if 'img' in req.FILES:
#                 save = form.save()
#                 img_instance = form.instance
#                 img_file = os.path.join(settings.MEDIA_ROOT, str(save.img))
            
#             image = img_instance
            
#             img_path = img_file
#             with Image.open(img_path) as img_obj:
#                 w, h = img_obj.size
#                 total = mul(w,h)
#                 img_colors = list(img_obj.getdata())
                
#                 # color_map_lab = {}
#                 # for key, val in color_map.items():
#                 #     color_map_lab[key] = rgb_to_lab(val)

#                 key_colors = list(color_map_lab.keys())
#                 val_colors = np.array(list(color_map_lab.values()))
#                 if img_obj.mode=='L':
#                     return render(req, 'show_color_shades.html',{'form':form,'msg':"The image is Grayscale."})
                
                
#                 lookup_lab_color = defaultdict()
                
               
#                 lab_st = t.time()
#                 img_colors_lab = []
#                 for clr in img_colors:
#                     if tuple(clr[:3]) in lookup_lab_color:
#                         val = lookup_lab_color[tuple(clr[:3])]
#                     else:
#                         val = rgb_to_lab(clr[:3])
#                         lookup_lab_color[tuple(clr[:3])] = val 
                    
#                     img_colors_lab.append(val)
                
#                 lab_en = t.time()
#                 print(f"\nlab_time: {lab_en-lab_st}\n")

#                 lookup = defaultdict(int)
#                 count_map = defaultdict(int)
                
#                 for clr in img_colors_lab:
                   
#                     if tuple(clr) in lookup:
#                         dist = lookup[tuple(clr)]
#                     else:
#                         dist = np.argmin(cdist(np.array(val_colors),np.array(clr).reshape(-1,3), metric = 'cityblock'))
#                         lookup[tuple(clr)] = dist
#                     count_map[key_colors[dist]]+=1
                
#                 res = {get_color(val):round((count_map[clr]/total)*100,2) for clr,val in color_map.items() if clr in count_map}
                
                   
#                 k = min(len(res), int(req.POST['drop_down']))
#                 res = dict(sorted(res.items(), key = lambda item: item[1], reverse=True)[:k])
               

#                 context = {
#                     'form': form,
#                     'image': image,
#                     'top_colors': res
#                 }

#             en = t.time()   
#             print(f"\ntime: {en-st}\n") 
#             return render(req, 'show_color_shades.html',context)
        
#     else:
#         form = UploadImage()
#     images = Upload.objects.all()
#     return render(req, 'show_color_shades.html',{"images":images,'form':form})

def fetch_colors(req):
    st = t.time()
    global img_file, img_instance
    
    if req.method == "POST":
        form = UploadImage(req.POST, req.FILES)
        if form.is_valid():
            if 'img' in req.FILES:
                save = form.save()
                img_instance = form.instance
                img_file = os.path.join(settings.MEDIA_ROOT, str(save.img))
            
            image = img_instance
            
            img_path = img_file
            
            with Image.open(img_path) as img_obj:
                w, h = img_obj.size
                total = mul(w,h)
                img_colors = list(img_obj.getcolors(maxcolors=256*256*256))
                
                
                
                img_colors_dict = {x[1]:x[0] for x in img_colors}
                
               
                if img_obj.mode=='L':
                    return render(req, 'show_color_shades.html',{'form':form,'msg':"The image is Grayscale."})
                
                count_map = defaultdict(int)
                for clr, cnt in img_colors_dict.items():
                    count_map[rgb_mapping[clr[:3]]] += cnt
                    
                                    
                
                #res = Counter({clr:round((count_map[clr]/total)*100,2) for clr,_ in count_map.items()})
                res = {}
                for clr,_ in count_map.items():
                    res[clr] = round((count_map[clr]/total)*100,2)
                res_st = t.time()
                res = Counter(res)
                
                res_en = t.time()
                print(f"res time: {res_en-res_st}")
                k = min(len(res), int(req.POST['drop_down']))
                res = dict(res.most_common(k))
                
                #res = dict(sorted(res.items(), key = lambda item: item[1], reverse=True)[:k])
                
                
                context = {
                    'form': form,
                    'image': image,
                    'top_colors': res
                }
           
            en = t.time()   
            print(f"\ntime: {en-st}\n") 
            return render(req, 'show_color_shades.html',context)
        
    else:
        form = UploadImage()
    images = Upload.objects.all()
    return render(req, 'show_color_shades.html',{"images":images,'form':form})