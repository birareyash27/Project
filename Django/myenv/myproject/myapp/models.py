from django.db import models


# Create your models here.
  
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    mobile=models.BigIntegerField()
    profile=models.ImageField(default="",upload_to="profile/")
    usertype = models.CharField(max_length=30,default="customer")

    def __str__(self):
        return  f"{self.name}"

class Tour(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tcategory = models.CharField(max_length=100,null=True, blank=True)
    tname = models.CharField(max_length=100)
    tprice = models.IntegerField()
    tlocation = models.CharField(max_length=255)
    days = models.IntegerField()
    desc = models.TextField()
    timage = models.ImageField(default="",upload_to="tour/")

    
