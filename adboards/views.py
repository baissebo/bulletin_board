from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions

from adboards.models import Ad, Review
from adboards.paginations import AdPagination
from adboards.serializers import AdSerializer, ReviewSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["title"]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
