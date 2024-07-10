
import os
from django.conf import settings

from django.shortcuts import render
from img_app.models import Upload
from .forms import UploadImage
from PIL import Image

import numpy as np

from collections import defaultdict

from .config_new import *
import time as t
# from pyciede2000 import ciede2000
from scipy.spatial.distance import cdist

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

def cie76(c1, c2):
    return np.linalg.norm(np.array(c1)-np.array(c2))

def cie2000(color1, color2):
    l1 = color1[0]
    a1 = color1[1]
    b1 = color1[2]
    l2 = color2[0]
    a2 = color2[1]
    b2 = color2[2]

    c1 = np.sqrt((a1**2.)+(b1**2.))
    c2 = np.sqrt((a2**2.)+(b2**2.))
    avg = np.average([c1,c2])
    g = 0.5 *(1. - np.sqrt((avg**7.)/((avg**7.)+(25.**7.))))
    a1p = (1.+g)*a1
    a2p = (1.+g)*a2
    c1p = np.sqrt((a1p**2.)+(b1**2.))
    c2p = np.sqrt((a2p**2.)+(b2**2.))
    if a1p == 0 and b1 == 0:
        h1p = 0
    else:
        if b1>=0:
            h1p = np.degrees(np.arctan2(b1,a1p))
        else:
            h1p =  np.degrees(np.arctan2(b1,a1p)) +360.
    if a2p == 0 and b2 == 0:
        h2p = 0
    else:
        if b2>=0:
            h2p = np.degrees(np.arctan2(b2,a2p))
        else:
            h2p =  np.degrees(np.arctan2(b2,a2p)) +360.
    dlp = l2 - l1
    dcp = c2p - c1p
    if h2p-h1p>180:
        dhc = 1
    elif h2p - h1p <-180:
        dhc = 2
    else:
        dhc = 0 
    if dhc == 0:
        dhp = h2p - h1p
    elif dhc == 1:
        dhp = h2p - h1p - 360.
    else:
        dhp = h2p + 360 - h1p
    dhp = 2. * np.sqrt(c1p*c2p)*np.sin(np.radians(dhp/2.))
    al = np.average([l1, l2])
    acp = np.average([c1p, c2p])
    if c1p*c2p == 0:
        hac = 3
    elif np.absolute(h2p-h1p) <= 180:
        hac = 0
    elif h2p+h1p < 360: 
        hac = 1
    else:
        hac = 2
    hap = np.average([h1p, h2p])
    if hac == 3:
        ahp = h1p+h2p
    elif hac == 0:
        ahp = hap
    elif hac == 1: 
        ahp = hap + 180
    else:
        ahp = hap - 180
    
    lpa50 = (al - 50)**2.
    sl = 1. + (0.015 * lpa50 / np.sqrt(20. + lpa50))
    sc = 1. + 0.045 * acp

    theta = 1. - 0.17 * np.cos(np.radians(ahp - 30.)) + 0.24 * np.cos(np.radians(2. * ahp)) + 0.32 * np.cos(np.radians(3. * ahp + 6.)) - 0.2 * np.cos(np.radians(4. * ahp - 63.))
    sh = 1. +  0.015 * acp * theta
    del_theta = 30. * np.exp(-1. * ((ahp-2.75)/25.)**2)
    rc = 2. * np.sqrt((acp**7.)/((acp**7.)+(25. **7.)))
    rtheta = -np.sin(np.radians(2. * del_theta))*rc
    fl = dlp / sl / 1.
    fc = dcp / sc / 1.
    fh = dhp / sh / 1.
    del2000 = np.sqrt(fl**2. + fc**2.  + rtheta*fc*fh)
    return del2000
    

def fetch_color_name(color, count_map,color_map_lab):
    
    #dist = [cie76(color, lab) for _,lab in color_map_lab.items()]
    dist = [np.linalg.norm(np.array(color)-np.array(lab)) for _, lab in color_map_lab.items()]
    key_colors = list(color_map_lab.keys())
    count_map[key_colors[np.argmin(dist)]]+=1
    return count_map

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

    # color = np.array(color)/255.0
    # val = color > 0.04045
    # color[val] = ((color[val] + 0.055)/1.055)**2.4
    # color[~val]/=12.92 
    # color*=100
    # weights = [[0.4124, 0.3576, 0.1805],
    #            [0.2126, 0.7152, 0.0722],
    #            [0.0193, 0.1192, 0.9505]]
    # xyz = np.dot(color,weights)
    # xyz/= [95.047, 100.0, 108.883]
    # val = xyz > 0.008856
    # xyz[val] = xyz[val] ** (1/3)
    # xyz[~val] = (7.787*xyz[~val]) + (16/116)
    # lab = np.zeros_like(xyz)
    # lab[0] = (116*xyz[1])-16
    # lab[1] = 500*(xyz[0]-xyz[1])
    # lab[2] = 200*(xyz[1]-xyz[2])
    return lab

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
                img_colors = list(img_obj.getdata())
                
                color_map_lab = {}
                for key, val in color_map.items():
                    color_map_lab[key] = rgb_to_lab(val)

                key_colors = list(color_map_lab.keys())
                val_colors = np.array(list(color_map_lab.values()))
                if img_obj.mode=='L':
                    return render(req, 'show_color_shades.html',{'form':form,'msg':"The image is Grayscale."})
                
                
                lookup_lab_color = defaultdict()
                
               
                lab_st = t.time()
                img_colors_lab = []
                for clr in img_colors:
                    if tuple(clr[:3]) in lookup_lab_color:
                        val = lookup_lab_color[tuple(clr[:3])]
                    else:
                        val = rgb_to_lab(clr[:3])
                        lookup_lab_color[tuple(clr[:3])] = val 
                    
                    img_colors_lab.append(val)
                
                lab_en = t.time()
                print(f"\nlab_time: {lab_en-lab_st}\n")

                lookup = defaultdict(int)
                count_map = defaultdict(int)
                
                for clr in img_colors_lab:
                    #count_map = fetch_color_name(clr, count_map, color_map_lab)
                    if tuple(clr) in lookup:
                        dist = lookup[tuple(clr)]
                    else:
                        #dist = np.argmin([np.sqrt(np.sum((val_colors-np.array(clr))**2, axis = 1))])
                        
                        dist = np.argmin(cdist(np.array(val_colors),np.array(clr).reshape(-1,3), metric = 'cityblock'))
                        lookup[tuple(clr)] = dist
                    count_map[key_colors[dist]]+=1
                
                res = {get_color(val):round((count_map[clr]/total)*100,2) for clr,val in color_map.items() if clr in count_map}
                
                   
                k = min(len(res), int(req.POST['drop_down']))
                res = dict(sorted(res.items(), key = lambda item: item[1], reverse=True)[:k])
               

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