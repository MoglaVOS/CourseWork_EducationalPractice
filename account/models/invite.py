from django.db import models

from account.models import User


class InviteManager(models.Manager):
    """ User Invites manager"""

    @staticmethod
    def get_invites_by_inviter(user):
        """ Return invites filtered by inviter """
        return Invite.objects.filter(inviter=user)

    @staticmethod
    def get_invites_by_invitee(user):
        """ Return invites filtered by invitee """
        return Invite.objects.filter(invitee_email=user.email)


class Invite(models.Model):
    """ User invitation into calendar model"""

    STATUS = (
        (0, "Ожидание ответа"),
        (1, "Принято"),
        (2, "Отказано")
    )

    # Fields
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invites")
    invitee_email = models.EmailField("Email Address", max_length=255, help_text="Ex: example@example.com",)
    status = models.IntegerField(choices=STATUS, default=0)

    objects = InviteManager()

    def __str__(self):
        return f"{self.invitee_email} - {self.status}"
