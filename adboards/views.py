from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import AllowAny

from adboards.models import Ad, Review
from adboards.paginations import AdPagination
from adboards.serializers import AdSerializer, ReviewSerializer
from users.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return (IsOwnerOrReadOnly,) if not self.request.user.role == "admin" else (IsAdminOrReadOnly,)
        elif self.request.method in ["GET"]:
            return (AllowAny,)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return (IsOwnerOrReadOnly,) if not self.request.user.role == "admin" else (IsAdminOrReadOnly,)
        elif self.request.method in ["GET"]:
            return (permissions.IsAuthenticated,)
        return super().get_permissions()
