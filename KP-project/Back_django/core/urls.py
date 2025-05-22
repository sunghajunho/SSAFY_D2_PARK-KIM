from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('movies/search/', views.search_movie),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
]
