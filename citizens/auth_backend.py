from django.contrib.auth.backends import BaseBackend
from kua import models
from kua.models import Members
from django.db.models import Q


class CitizenAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            member = Members.objects.get(Q(email=username) | Q(nssfcardnumber=username))

            if member.krapin == password:
                return member
        except Members.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Members.objects.get(pk=user_id)
        except Members.DoesNotExist:
            return None
