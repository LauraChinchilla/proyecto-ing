from django.db import models
from store.models import Product


# Create your models here.


class Favorite(models.Model):
    favorite_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.favorite_id

class FavoriteItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price*self

    def __unicode__(self):
        return self.product
