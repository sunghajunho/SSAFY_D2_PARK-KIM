from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'follows', views.FollowViewSet)

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
]

