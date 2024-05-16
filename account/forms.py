from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from account.models.user import User


class SignInForm(forms.Form):
    """ User sign in form """
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class SignUpForm(forms.ModelForm):
    """ User Sing Up Form"""
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password_check = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "second_name", "surname", "position", "department"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "second_name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"})
        }

    def password_match(self):
        """ Check password quality and consistency """
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password")
        if password and password_check and password != password_check:
            raise ValidationError("Password didn't match!")
        return password

    def save(self, commit=True):
        """ Encrypt password and save user """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
