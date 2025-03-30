from django.db import models
from django.contrib.auth.models import User
from PIL import Image
#from phone_field import PhoneField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    about = models.TextField(blank=True,null=True)
    email = models.EmailField(blank = True,null = True)
    school = models.CharField(max_length=70,blank=True,null=True)
    college = models.CharField(max_length=70,blank=True,null=True)
    work = models.CharField(max_length=70,blank=True,null=True)
    skills = models.CharField(max_length=70,blank=True,null=True)
    current_city = models.CharField(max_length=70,blank=True,null=True)
#    phon_no = PhoneField(max_length=12,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    birth_day = models.DateField(blank=True,null=True)
    otp = models.IntegerField(blank=True,null=True)
    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
    )
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (60,60)
            img.thumbnail(output_size)
            img.save(self.image.path)
