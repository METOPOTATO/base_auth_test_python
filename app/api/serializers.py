from rest_framework import serializers
import uuid
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        pw = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if pw is not None:
            instance.set_password(pw)
            instance.is_active = False
            instance.token = str(uuid.uuid3(
                uuid.NAMESPACE_OID, instance.email))
            instance.save()

        return instance
