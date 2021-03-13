from rest_framework import serializers
from rest_framework import fields
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)
    password = fields.CharField(write_only=True)
    confirm_password = fields.CharField(write_only=True)

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
    )

        validated_data['group'].user_set.add(user)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password', 'group']


class UserLoginSerializer(serializers.ModelSerializer):
    password = fields.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
