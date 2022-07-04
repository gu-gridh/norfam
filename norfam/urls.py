from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/terms', views.TermViewSet, basename="term")
router.register(r'api/termsim', views.TermsimViewSet, basename="termsim")
router.register(r'api/entities', views.EntityViewSet, basename="entity")
router.register(r'api/documents', views.DocumentViewSet, basename="document")
router.register(r'api/query', views.QueryViewSet, basename="api")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]