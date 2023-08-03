from rest_framework import viewsets
from .permissions import IsSuperUserOrReadOnly


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True)

        return queryset
