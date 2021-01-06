from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_planets, name='planet-list'),
    path('update_favourite/<int:swapi_id>/<str:planet_name>/', views.update_favourite, name='update-favourite-planet'),
]