from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # ID ist jetzt direkt drin → wird automatisch von Django vergeben
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        # User mit create_user erstellen
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # User-Infos mit ID und Registrierungsdatum
        fields = ["id", "email", "username", "date_joined"]