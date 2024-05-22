from django.urls import path
from account import views


app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("change_password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("invite/", views.UserInviteView.as_view(), name="invite"),
    path("invite/delete/", views.invite_delete, name="invite_delete"),
    path("invite/decline/", views.invite_decline, name="invite_decline"),
    path("invite/accept/", views.invite_accept, name="invite_accept"),
]
