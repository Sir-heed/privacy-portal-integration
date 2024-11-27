from django.urls import include, path
from rest_framework import routers

from . import views


app_name = 'ums'

router = routers.DefaultRouter()

router.register(prefix='', viewset=views.UserViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("callback", views.redirect_uri, name="detail"),
    path(route=f'{app_name}/', view=include((router.urls, app_name), namespace=app_name)),
]
