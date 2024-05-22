from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from account.models import User
from account.models import Invite
from event.models.notification import Notification


class SignInForm(forms.Form):
    """ User sign in form """
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        """ Return cleaned data and check for email & password correctness """
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                self.add_error("password", "Неверный адрес электронной почты или пароль!")
                raise ValidationError("Authentication error")
            if not user.is_active:
                self.add_error("password", "Этот аккаунт неактивен!")
                raise ValidationError("User is not active error")

        return cleaned_data


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

    def clean(self):
        """ Return cleaned data and check password quality and consistency """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_check = cleaned_data.get("password_check")
        if password and password_check and password != password_check:
            self.add_error("password_check", "Пароли не совпадают!")
        return cleaned_data

    def save(self, commit=True):
        """ Encrypt password and save user """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    """ Change user password form """
    password_old = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password_new = forms.CharField(
        label="Password new",
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
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ Check password quality and consistency """
        cleaned_data = super().clean()

        # Wrong old password
        password_old = cleaned_data.get("password_old")
        if not self.user.check_password(password_old):
            self.add_error("password_old", "Неправильный пароль!")
            raise ValidationError("Wrong old password!")

        # Old password != new password
        password_new = cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")
        if password_new and password_old and password_old == password_new:
            self.add_error("password_new", "Новый пароль не должен совпадать с старым!")
            raise ValidationError("Password equals to old password!")

        # Password != Password check
        if password_new and password_check and password_new != password_check:
            self.add_error("password", "Пароли не совпадают!")
            raise ValidationError("Password didn't match!")

        return cleaned_data

    def save(self, commit=True):
        """ Encrypt new password and update user """
        self.user.set_password(self.cleaned_data["password_new"])
        if commit:
            self.user.save()
        return self.user


class UserInviteForm(forms.ModelForm):
    """ User calendar invitation form """

    class Meta:
        model = Invite
        fields = ["invitee_email"]
        widgets = {
            "invitee_email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.inviter = kwargs.pop('inviter', None)
        super(UserInviteForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ Check if invitee exists. Return cleaned_data """
        cleaned_data = super().clean()
        invitee_email = cleaned_data.get("invitee_email")

        # Handle Invitee Does Not Exist Error
        try:
            User.objects.get(email=invitee_email)
        except User.DoesNotExist:
            self.add_error("invitee_email", "Пользователя с такой почтой не существует")
            raise ValidationError("User Does Not Exist")

        # Handle Inviter == Invitee Error
        if self.inviter and self.inviter.email == invitee_email:
            self.add_error("invitee_email", "Нельзя отправить приглашение самому себе")
            raise ValidationError("Invitee shouldn't be equal to inviter")

        # Handle Not Unique Inviter-Invitee pair Error
        if Invite.objects.filter(inviter=self.inviter, invitee_email=invitee_email).exists():
            self.add_error("invitee_email", "Приглашение уже было отправлено")
            raise ValidationError("Invite already sent")

        return cleaned_data

    def save(self, commit=True):
        invite = super().save(commit=False)
        Notification.objects.create(
            user=User.objects.get(email=invite.invitee_email),
            title="Приглашение в календарь",
            description=f"{self.inviter.second_name} {self.inviter.first_name} пригласил вас в свой календарь.",
            url="event:dashboard",
            event=None
        )
        if commit:
            invite.save()
        return invite
