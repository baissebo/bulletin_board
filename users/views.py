from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config import settings
from users.models import User
from users.serializers import UserSerializer


# @api_view(["POST"])
# def reset_password(request):
#     email = request.data.get("email")
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"error": "Пользователь не найден!"}, status=status.HTTP_404_NOT_FOUND)
#
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     host = request.get_host()
#     reset_link = f"http://{host}/users/reset-password/{uid}/{token}/"
#
#     send_mail(
#         "Сброс пароля",
#         f"Перейдите по ссылке для сброса пароля: {reset_link}",
#         settings.EMAIL_HOST_USER,
#         [user.email],
#         fail_silently=False,
#     )
#
#     return Response({"message": "Ссылка для сброса пароля отправлена на вашу почту."},
#                     status=status.HTTP_200_OK)
#
#
# @api_view(["POST"])
# def reset_password_confirm(request):
#     uid = request.data.get("uid")
#     token = request.data.get("token")
#
#     try:
#         uid = urlsafe_base64_decode(uid).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         return Response({"error": "Токен или идентификатор некорректны!"}, status=status.HTTP_400_BAD_REQUEST)
#
#     if not default_token_generator.check_token(user, token):
#         return Response({"error": "Неверный токен!"}, status=status.HTTP_401_UNAUTHORIZED)
#
#     new_password = request.data.get("new_password")
#     user.set_password(new_password)
#     user.save()
#
#     return Response({"message": "Пароль успешно сброшен"}, status=status.HTTP_200_OK)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
