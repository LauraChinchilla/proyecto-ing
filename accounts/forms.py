from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Ingrese Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirmar Password',
        'class': 'form-control',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese Nombre',
        'class': 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese Apellidos',
        'class': 'form-control',
    }))

    phone_nomber = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese No. de Telefono',
        'class': 'form-control',
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese Email',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name', 'phone_nomber', 'email', 'password']


    def __int__(self, *args, **kwargs):
        super(RegistrationForm, self).__int__(*args,**kwargs)
        #ESTA PARTE NO FUNCIONA

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'



    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "La contraseña no coincide"
            )
