from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_desc = models.CharField(max_length=500, default='desc')
    product_category = models.CharField(max_length=200, default="")
    product_subcategory = models.CharField(max_length=200, default="")
    product_price = models.IntegerField(default=0)
    product_date = models.DateField()
    product_image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=5000, default="")

    def __str__(self):
        return self.name