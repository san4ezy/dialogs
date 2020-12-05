from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), required=False)
    password = serializers.CharField(label=_("Password"), required=False, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not (email and password):
            raise serializers.ValidationError('Phone number and Password are required')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return user.make_token()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'birthday',)

    def create(self, validated_data):
        model = self.Meta.model
        user = model.objects.create(**validated_data)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password') if 'password' in validated_data else None
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SignupUserSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'password', 'first_name', 'last_name',)
        extra_kwargs = {
            'phone_number': {'required': True, 'allow_null': False},
            'password': {'required': True, 'allow_null': False},
        }
