from django.db import models



class GUser(models.Model):
    gender = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    user_id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150, unique=True)
    dob = models.DateField()
    sex = models.CharField(max_length=15, choices=gender, default="Male")
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

class SUser(models.Model):
    gender = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    user_id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150, unique=True)
    dob = models.DateField()
    sex = models.CharField(max_length=15, choices=gender, default="Male")
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.user_id)

class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    stock = models.IntegerField()
    catagorey = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='')

    class Meta:
        ordering = ['-item_name']

    def __str__(self):
        return "{}".format(self.item_name)

class Temp(models.Model):
    cid = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255, null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)

class Cart(models.Model):
    uid = models.ForeignKey(GUser, on_delete=models.CASCADE)
    data = models.ManyToManyField(Temp)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=255, null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)

class Order_Final(models.Model):
    uid = models.ForeignKey(GUser, on_delete=models.CASCADE)
    oid = models.ManyToManyField(Order)