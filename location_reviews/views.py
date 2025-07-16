from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Location, LocationCategories, Review
from .serializers import LocationCategoriesSerializer, LocationSerializer, ReviewSerializer
import pandas as pd
from .permissions import IsAuthenticatedOrAdminForUnsafe, IsAuthenticatedOrAdminOwnerForUnsafe
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrAdminOwnerForUnsafe]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['rating', 'categories']
    search_fields = ['=name', 'description']

    @method_decorator(cache_page(60*5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*5))
    @action(detail=False, methods=['get'])
    def export(self, request):
        export_format = request.query_params.get('type', 'json')
        locations = self.get_queryset()
        if export_format == 'csv':
            data = []
            for loc in locations:
                data.append({
                    'id': loc.id,
                    'name': loc.name,
                    'description': loc.description,
                    'rating': loc.rating,
                    'address': str(loc.address),
                    'categories': ','.join([cat.name for cat in loc.categories.all()])
                })
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="locations.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response
        else:  
            serializer = self.get_serializer(locations, many=True)
            return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrAdminOwnerForUnsafe]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @method_decorator(cache_page(60*5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        review = self.get_object()
        review.likes += 1
        review.save()
        return Response({'id':review.pk, 'likes': review.likes, 'dislikes': review.dislikes})

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        review = self.get_object()
        review.dislikes += 1
        review.save()
        return Response({'id':review.pk, 'likes': review.likes, 'dislikes': review.dislikes})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = LocationCategories.objects.all()
    serializer_class = LocationCategoriesSerializer
    permission_classes = [IsAuthenticatedOrAdminForUnsafe]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @method_decorator(cache_page(60*5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


