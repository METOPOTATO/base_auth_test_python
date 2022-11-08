from rest_framework import serializers
import uuid
from .models import User
from .utils.common_functions import _validate_email, _validate_password


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

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

    def validate(self, instance):
        validate_email = _validate_email(instance['email'])
        if validate_email is not True:
            raise serializers.ValidationError(validate_email)

        validate_password = _validate_password(instance['password'])
        if validate_password is not True:
            raise serializers.ValidationError(validate_password)
        return instance
