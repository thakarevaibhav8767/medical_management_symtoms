from django.db import models
import datetime
class admin1(models.Model):
    Admin_Id=models.IntegerField(primary_key=True)
    Admin_Name=models.CharField(max_length=25,null=False)
    Admin_password=models.CharField(max_length=16)
class customer(models.Model):
    User_Id = models.IntegerField(primary_key=True)
    User_Name=models.CharField(max_length=25)
    Password=models.CharField(max_length=16)
    Gender=models.CharField(max_length=10)
    Phone_Number=models.IntegerField()
    Email=models.CharField(max_length=25)

class orderdetails(models.Model):
    User_Id=models.IntegerField()
    User_Name=models.CharField(max_length=30)
    Phone_Number=models.IntegerField()
    medicines_names = models.CharField(max_length=200)
    quantity = models.IntegerField()
    Date = models.DateField(default=datetime.date.today)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)



class medicines(models.Model):
    med_Id=models.IntegerField(primary_key=True)
    med_Name=models.CharField(max_length=30)
    Available_quantity=models.IntegerField()
    Price=models.DecimalField(max_digits=10,decimal_places=2)
    mfg_Date=models.DateField()
    Exp_Date=models.DateField()
class diseas(models.Model):
    diseas1=models.CharField(max_length=50)
    medicines=models.CharField(max_length=100,default="No medicine prescribed")

class purchase(models.Model):
    User_Id=models.IntegerField()
    med_id=models.IntegerField()
    med_name=models.CharField(max_length=40)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField(default=datetime.date.today)




# Create your models here.
