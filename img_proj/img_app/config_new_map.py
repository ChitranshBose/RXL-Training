import pickle as pk
import gzip


with gzip.open('/home/chitranshbose/Downloads/python_prac/django/img_proj/img_app/rgb_mapping.pkl.gz', 'rb') as f:
    rgb_mapping = pk.load(f)

print("model loaded")