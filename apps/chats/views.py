from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .filters import DialogFilteringBackend
from .models import Message, Dialog


class DialogPagination(PageNumberPagination):
    page_size = 20


class DialogViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Dialog source
    """
    queryset = Dialog.objects.prefetch_related('favoritedialog_set')
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DialogSerializer
    parser_classes = (JSONParser,)
    pagination_class = DialogPagination
    filter_backends = (DialogFilteringBackend,)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(users__contains=[user.pk])

    @action(methods=['PATCH'], detail=True)
    def add_to_favorite(self, request, pk=None, *args, **kwargs):
        dialog = get_object_or_404(self.get_queryset(), pk=pk)
        dialog.add_to_favorite(request.user)
        dialog.refresh_from_db()
        serializer = serializers.DialogSerializer(instance=dialog)
        return Response(serializer.data)

    @action(methods=['GET', 'POST'], detail=True)
    def messages(self, request, pk=None, *args, **kwargs):
        dialog = self.get_object()
        if request.method == 'GET':
            messages = dialog.messages.order_by('created')  # it would be nice to have pagination here
            last_message = messages.last()
            last_message.mark_as_read()
            serializer = serializers.MessageSerializer(messages, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = serializers.SendMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            msg = dialog.send_message(sender=request.user, text=serializer.validated_data['text'])
            return Response(serializers.MessageSerializer(instance=msg).data)


class MessagePagination(PageNumberPagination):
    page_size = 20


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """Messages source
    """
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MessageSerializer
    parser_classes = (JSONParser,)
    pagination_class = MessagePagination
