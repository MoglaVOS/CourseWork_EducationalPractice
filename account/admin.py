from django.contrib import admin

from account.models.invite import Invite
from account.models.user import User


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ["inviter", "invitee_email", "status"]
    search_fields = ["inviter", "invitee_email"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name", "second_name", "surname", "email",
        "position", "department", "is_staff", "is_superuser"
    ]
    readonly_fields = ["is_staff", "is_superuser"]
    search_fields = ["first_name", "second_name", "surname", "email"]