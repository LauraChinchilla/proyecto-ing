from django import forms
from .models import ReviewRating, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

class RegistrationProduct(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese Nombre del Inmueble',
        'class': 'form-control',
    }))

    slug = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ejem = casa-de-venta-lugardeventa',
        'class': 'form-control',
    }))

    # description = forms.TextField(widget=forms.TextInput(attrs={
    #     'placeholder':'Ingrese Descripcion',
    #     'class': 'form-control',
    # }))

    price = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese Precio del Inmueble',
        'class': 'form-control',
    }))

    # images = CloudinaryField(required=False, error_messages = {'invalid': ('Solo archivos de imagen')}, widget=forms.FileInput)

    stock = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese cantidad a vender',
        'class': 'form-control',
    }))

    # category = forms.ModelChoiseField()

    class Meta:
        model = Product
        fields = ['product_name','slug', 'descripton', 'price', 'images', 'stock', 'is_available', 'category']


    def __int__(self, *args, **kwargs):
        super(RegistrationProduct, self).__int__(*args,**kwargs)
        #ESTA PARTE NO FUNCIONA

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
