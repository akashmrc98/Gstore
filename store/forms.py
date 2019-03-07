from django import forms
from .models import GUser, Items

class Login_Form(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "enter email", "class": "form-control fnsbig"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "enter password", "class": "form-control fnsbig"}
        )
    )


class Change_Password_Form(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "enter email", "class": "form-control fnsbig"}
        )
    )

    password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "enter password", "class": "form-control fnsbig"}
        )
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "enter password", "class": "form-control fnsbig"}
        )
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "enter password", "class": "form-control fnsbig"}
        )
    )

    def clean(self):
        cleaned_data = super(Change_Password_Form, self).clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class Add_User_Form(forms.Form):
    class Meta:  
        model = GUser
        fields = "__all__"

    gender = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control fnsbig","placeholder": "enter name",})
    )

    dob = forms.DateField(
        label="date",
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={"class":"form-control","placeholder": "dd/mm/yyyy",}
        )
    )
    sex = forms.ChoiceField(
        choices=gender, widget=forms.RadioSelect(attrs={"class": "ritem form-radio"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control fnsbig","placeholder": "enter phone",})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "enter email", "class": "form-control fnsbig"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "enter password", "class": "form-control fnsbig"}
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "enter address", "class": "form-control fnsbig", "rows":3}
        )
    )

class Item_Form(forms.ModelForm):
    class Meta:
        model = Items
        fields = "__all__"

    item_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control fnsbig","placeholder": "enter item name",})
    )

    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control fnsbig","placeholder": "enter stock",})
    )

    catagorey = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control fnsbig","placeholder": "enter catagorey",})
    )

    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control fnsbig","placeholder": "enter price",})
    )

    image  = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control-file fnsbig"})
    )