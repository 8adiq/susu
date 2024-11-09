from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        """function for creating new user instance"""
        user = User.objects.create(
            email = validated_data.get('email'),
            username = validated_data.get('username'),
            role = validated_data.get('role')
        )
        user.set_password(validated_data.get('password')) # password hashed.
        user.save()
        return user
