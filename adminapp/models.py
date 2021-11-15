from django.db import models
# from django.core.files.storage import FileSystemStorage
from datetime import date
# Create your models here.
# fs = FileSystemStorage(location="/media/ebook")
class Bookstbl(models.Model):
    Name = models.CharField(max_length=50)	
    Publication	= models.CharField(max_length=50)	
    Author = models.CharField(max_length=50)	
    Category = models.CharField(max_length=50)	
    AvailableCopies	= models.IntegerField()	
    IssuedCopies = models.IntegerField()	
    TotalCopies	= models.IntegerField()
    Book_cover = models.ImageField(upload_to='book_covers',default='-')
    isebook = models.BooleanField(default=False)
    Pdf_file = models.FileField(upload_to='ebook',default='-')
    # Pdf_file = models.FileField(storage=fs,default='-')
    admin = models.ForeignKey('Adminstbl', verbose_name=(""), on_delete=models.CASCADE)
	
        
class Adminstbl(models.Model):
    Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50,default='-')
    Mobile = models.CharField(max_length=50,default='-')
    Address = models.CharField(max_length=80,default='-')
    Birthday = models.DateField(default=date.today())
    Joining_date = models.DateField(default=date.today())
    Profile_pic = models.ImageField(upload_to='admin_profile_pic',default='-')
    adminEmail = models.CharField(max_length=50, primary_key=True)
    Password = models.CharField(max_length=50)
    Orgnization = models.CharField(max_length=50)


class Userstbl(models.Model):
    Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50,default='-')
    Mobile = models.CharField(max_length=50,default='-')
    Address = models.CharField(max_length=80,default='-')
    Birthday = models.DateField(default=date.today())
    Joining_date = models.DateField(default=date.today())
    Profile_pic = models.ImageField(upload_to='profile_pic',default='-')
    userEmail = models.CharField(max_length=50, primary_key=True)
    Password = models.CharField(max_length=50)
    admin = models.ForeignKey('Adminstbl', verbose_name=(""), on_delete=models.CASCADE)
    
