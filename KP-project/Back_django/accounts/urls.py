from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'follows', views.FollowViewSet)

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
