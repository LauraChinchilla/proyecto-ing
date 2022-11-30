from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from favorites.models import FavoriteItem
from favorites.views import _favorite_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm, RegistrationProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def registerProduct(request):#crear producto
    form_product = RegistrationProduct()
    if request.method == 'POST':
        form_product = RegistrationProduct(request.POST)
        if form_product.is_valid():
            product_name = form.cleaned_data['product_name']
            slug = form.cleaned_data['slug']
            descripton = form.cleaned_data['descripton']
            price = form.cleaned_data['price']
            images = form.cleaned_data['images']
            stock = form.cleaned_data['stock']
            category = form.cleaned_data['category']

            product = Product.objects.create_product(product_name=product_name, slug=slug, descripton=descripton, price=price, images=images, stock=stock, category=category)
            product.save()

    context = {
        'form_product': form_product
    }
    return render(request, 'store/publication.html', context)

def store(request, category_slug=None ):##
    categories = None
    products = None
    #price_product = None##

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        #price_product = get_object_or_404(Product, price = price_product_slug)##
        products = Product.objects.filter(category=categories , is_available=True).order_by('id')##
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    context = {
        'products':paged_products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_favorite = FavoriteItem.objects.filter(favorite__favorite_id=_favorite_id(request), product=single_product).exists()
    except Exception as e:
        raise e


    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product':single_product,
        'in_favorite':in_favorite,
        'reviews':reviews,
        'product_gallery':product_gallery,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(descripton__icontains=keyword) | Q(product_name__icontains=keyword)   )
            product_count = products.count()


    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

@login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas Gracias, tu comentario ha sido actualizado')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Muchas Gracias, tu comentario fue enviado con exito')
                return redirect(url)
