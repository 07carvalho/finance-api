from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authy.serializers import LoginSerializer, SignUpSerializer


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = authenticate(
                username=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
            if user and user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            return Response(
                {"error": "Email or password wrong."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"login_error": "Email or password wrong."})


class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        token = Token.objects.get(user=user)
        token.delete()
        return Response({"message": "You are logged out"}, status=status.HTTP_200_OK)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = self.get_serializer().create(serializer.validated_data)
        token, created = Token.objects.get_or_create(user=new_user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
