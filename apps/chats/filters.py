from rest_framework import filters


class DialogFilteringBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        last_sent = request.query_params.get('last_sent')
        last_received = request.query_params.get('last_received')
        user = request.user
        if last_sent and user.is_authenticated:
            queryset = queryset.last_sent(user=user)
        if last_received and user.is_authenticated:
            queryset = queryset.last_received(user=user)
        return queryset
