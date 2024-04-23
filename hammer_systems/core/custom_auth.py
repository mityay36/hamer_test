from django.contrib.auth.backends import ModelBackend, UserModel
from rest_framework.generics import get_object_or_404


class AuthenticationWithoutPassword(ModelBackend):

    def authenticate(self, request, phone_number=None):
        if phone_number is None:
            phone_number = request.data.get('phone_number', '')
        return get_object_or_404(UserModel, phone_number=phone_number)

    def get_user(self, user_id):
        return get_object_or_404(UserModel, pk=user_id)
