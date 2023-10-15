from django.db import models
from .fields import PathField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    path = PathField()
    image = models.ImageField(upload_to="categories/logo", null=True, blank=True)

    class Meta:
        get_latest_by = 'created_at'


class Brand(BaseModel):
    name = models.CharField(max_length=511, null=False, blank=False)
    description = models.TextField()
    image = models.ImageField(upload_to="brands/logo", null=True, blank=True)


class Product(BaseModel):
    name = models.CharField(max_length=511, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.PROTECT)

    class Meta:
        get_latest_by = 'created_at'


class ProductImage(BaseModel):
    image = models.ImageField(upload_to="products/images")
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    updated_at = None

    class Meta:
        get_latest_by = 'created_at'
