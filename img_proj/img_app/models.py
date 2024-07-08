from django.db import models as md

# Create your models here.

CHOICE=[tuple([i,i]) for i in range(1,21)]

class Upload(md.Model):
    img = md.ImageField(upload_to='pictures', blank=True, null=True)
    drop_down = md.IntegerField(choices = CHOICE, default = 1)