from django.urls import path, include
from rest_framework import routers
from . import views
import diana.utils as utils


router = routers.DefaultRouter()
endpoint = utils.build_app_endpoint("norfam")
documentation = utils.build_app_api_documentation("norfam", endpoint)


router = routers.DefaultRouter()

router.register(rf'{endpoint}/terms', views.TermViewSet, basename="term")
router.register(rf'{endpoint}/termsim', views.TermsimViewSet, basename="termsim")
router.register(rf'{endpoint}/entities', views.EntityViewSet, basename="entity")
router.register(rf'{endpoint}/documents', views.DocumentViewSet, basename="document")
router.register(rf'{endpoint}/query', views.QueryViewSet, basename="api")

urlpatterns = [
    path('', include(router.urls)),

    *documentation,

    # Automatically generated views
    *utils.get_model_urls('norfam', f'{endpoint}', exclude=['page', 'work', 'work_authors']),
    path(f'{endpoint}/api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]