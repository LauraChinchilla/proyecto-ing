from django.shortcuts import render, redirect
from store.models import Product
from .models import Favorite, FavoriteItem
# Create your views here.



def _favorite_id(request):
    favorite = request.session.session_key
    if not favorite:
        favorite = request.session.create()
    return favorite


def add_favorite(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        favorite = Favorite.objects.get(favorite_id=_favorite_id(request))
    except Favorite.DoesNotExist:
        favorite = Favorite.object.create(
            favorite_id = _favorite_id(request)
        )
    favorite.save()

    try:
        favorite_item = FavoriteItem.object.get(product=product, favorite=favorite)
        favorite_item.quantity +=1
        favorite_item.save()
    except FavoriteItem.DoesNotExist:
        favorite_item = FavoriteItem.object.create(
            product = product,
            quantity = 1,
            favorite = favorite,
        )
        favorite_item.save()

    return redirect('favorite')


def favorite(request):
    return render(request, 'store/favorite.html')
