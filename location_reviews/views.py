from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from .models import Location, LocationCategories, Review
from .serializers import LocationCategoriesSerializer, LocationSerializer, ReviewSerializer


# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['rating', 'categories']
    search_fields = ['name', 'description']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        review = self.get_object()
        review.likes += 1
        review.save()
        return Response({'likes': review.likes, 'dislikes': review.dislikes})

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        review = self.get_object()
        review.dislikes += 1
        review.save()
        return Response({'likes': review.likes, 'dislikes': review.dislikes})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = LocationCategories.objects.all()
    serializer_class = LocationCategoriesSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]