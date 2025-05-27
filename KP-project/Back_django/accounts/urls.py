from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'follows', views.FollowViewSet)

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='my-profile'), 
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('profile/image/delete/',views.delete_profile_image, name='delete_profileimage'),
    path('history/check/<int:tmdb_id>/', views.WatchHistoryCheckView.as_view(), name='watch-history-check'),
    path('history/add/', views.WatchHistoryAddView.as_view(), name='watch-history-add'),
    path('history/remove/<int:tmdb_id>/', views.WatchHistoryRemoveView.as_view(), name='watch-history-remove'),
    path('favorites/check/<int:tmdb_id>/', views.FavoriteCheckView.as_view(), name='favorite-check'),
    path('favorites/add/', views.FavoriteAddView.as_view(), name='favorite-add'),
    path('favorites/remove/<int:tmdb_id>/', views.FavoriteRemoveView.as_view(), name='favorite-remove'),
    path('favorite-movies/', views.FavoriteMovieListView.as_view(), name='my-favorite-movie-list'),
    path('favorite-movies/<str:username>/',views.FavoriteMovieListView.as_view(), name='favorite-movie-list'),
    path('accounts/delete/', views.AccountDeleteView.as_view(), name='account-delete'),
]

