from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorite, name='favorite'),
    path('add_favorite/int:product_id', views.add_favorite, name='add_favorite'),
]
