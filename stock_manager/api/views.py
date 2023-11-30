from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Deals, Bonds
from .serializers import DealsSerializer, BondsSerializer


class DealsViewSet(viewsets.ModelViewSet):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BondsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
