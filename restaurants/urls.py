from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/<int:cityId>/<city>', views.search, name="search")
]
