from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.chats.models import Message, Dialog
from apps.users.serializers import UserSerializer


class DialogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    participants = UserSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = ('id', 'participants', 'users', 'user_id', 'is_favorite',)
        extra_kwargs = {
            'users': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        creator_id = self.context['request'].user.pk
        user_id = validated_data.pop('user_id')
        validated_data['users'] = [creator_id, user_id]
        return super().create(validated_data)

    def get_is_favorite(self, obj):
        return obj.is_favorite  # must be prefetched in queryset


class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    dialog = DialogSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'dialog', 'text', 'is_read', 'created',)
