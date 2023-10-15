from collections.abc import Iterable
from django.db import models
from .fields import PathField
from django.contrib.postgres.indexes import GistIndex
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    # Think how should update and deletes should be handled
    path = PathField()
    image = models.ImageField(upload_to="categories/logo", null=True, blank=True)

    class Meta:
        get_latest_by = 'created_at'
        indexes = [
            GistIndex(fields=['path'], name='path_gist_idx')
        ]

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        # Maybe add a trigger function
        # Capitalize all ancestors
        self.path = '.'.join(x.capitalize() for x in self.path.split('.'))
        ancestors = self.path[:-1]

        if not self.objects.filter(path__startswith=ancestors).first():
            raise ValidationError(
                _('Invalid ancestors ("%(ancestors)s") for path "%(path)s".'),
                params={'ancestors': ancestors, 'path': self.path})

        return super().save(force_insert, force_update, using, update_fields)


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
