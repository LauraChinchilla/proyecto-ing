from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.db import models #cloudinary
from cloudinary.models import CloudinaryField #cloudinary

class createProducto():
        def create_product(product_name, slug, descripton, price, images, stock, is_available, category):#crear producto

            product = self.model(
                product_name = product_name,
                slug = slug,
                descripton = descripton,
                price = price,
                images = images,
                stock = stock,
                is_available = is_available,
                category = category,
            )

            product.save(using=self._db)
            return product



# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    descripton = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = CloudinaryField('image')
    stock = models.IntegerField()
    is_available = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = createProducto()

    def get_url(self):
        return reverse('products_by_price', args=[self.slug])

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

#class ProductGallery(models.Model):
#    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
#    image = models.ImageField(upload_to='store/products', max_length=255)
#
#    def __str__(self):
#        return self.product.product_name
