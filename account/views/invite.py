from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from account.forms import UserInviteForm
from account.models import Invite


class UserInviteView(LoginRequiredMixin, View):
    """ User Invitation into calendar view """

    login_url = "account:signin"
    template_name = "invite.html"
    form_class = UserInviteForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, inviter=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.inviter = request.user
            form.save()
            return redirect("event:dashboard")

        context = {"form": form}
        return render(request, self.template_name, context)


def invite_delete(request):
    if request.method == "POST":
        invite_id = request.POST.get("invite_id")
        try:
            invite = Invite.objects.get(id=invite_id)
            invite.delete()
            return JsonResponse({"message": "Приглашение успешно удалено"})
        except Invite.DoesNotExist:
            return JsonResponse({"message": "Приглашения не существует"})
    else:
        return JsonResponse({"message": "Метод не поддерживается"})


def invite_decline(request):
    if request.method == "POST":
        invite_id = request.POST.get("invite_id")
        try:
            invite = Invite.objects.get(id=invite_id)
            invite.status = 2
            invite.save()
            return JsonResponse({"message": "Вы отказались от приглашения"})
        except Invite.DoesNotExist:
            return JsonResponse({"message": "Приглашения не существует"})
    else:
        return JsonResponse({"message": "Метод не поддерживается"})


def invite_accept(request):
    if request.method == "POST":
        invite_id = request.POST.get("invite_id")
        try:
            invite = Invite.objects.get(id=invite_id)
            invite.status = 1
            invite.save()
            return JsonResponse({"message": "Вы приняли приглашение"})
        except Invite.DoesNotExist:
            return JsonResponse({"message": "Приглашения не существует"})
    else:
        return JsonResponse({"message": "Метод не поддерживается"})
