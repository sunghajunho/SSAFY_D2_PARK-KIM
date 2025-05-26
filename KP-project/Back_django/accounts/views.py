from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from .serializers import CustomUserSerializer, FollowSerializer, WatchHistorySerializer
from .models import CustomUser, Follow, WatchHistory, FavoriteMovie
from core.models import Genre
from rest_framework import status, viewsets, generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        if username:
            user = get_object_or_404(get_user_model(), username=username)
        else:
            user = request.user
        
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        following_id = self.request.data.get('following')
        if following_id == str(self.request.user.id):
            raise serializers.ValidationError("자기 자신을 팔로우할 수 없습니다.")
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        following_id = request.data.get('following')
        print(following_id)
        try:
            following_user = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'})
        return Response({'status': 'followed'})
    
    @action(detail=False, methods=['get'], url_path='status/(?P<username>[^/.]+)')
    def follow_status(self, request, username=None):
        user = get_object_or_404(CustomUser, username=username)
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        return Response({'is_following': is_following})

    @action(detail=False, methods=['get'], url_path='followers/(?P<username>[^/.]+)')
    def followers(self, request, username=None):
        user = get_object_or_404(CustomUser, username=username)
        followers = user.followers.values_list('follower__username', flat=True)
        return Response({'followers': list(followers)})

    @action(detail=False, methods=['get'], url_path='following/(?P<username>[^/.]+)')
    def following(self, request, username=None):
        user = get_object_or_404(CustomUser, username=username)
        following = user.following.values_list('following__username', flat=True)
        return Response({'following': list(following)})


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all().values('id', 'name')
        return Response(genres)
    
# views.py
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):
    user = request.user
    user.profile_image.delete(save=False)
    user.profile_image='default_profile.jpg'
    user.save()
    return Response({'status': 'profile image deleted'}, status=200)

class WatchHistoryCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tmdb_id):
        seen = WatchHistory.objects.filter(user=request.user, tmdb_id=tmdb_id).exists()
        return Response({"seen": seen})

class WatchHistoryAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WatchHistorySerializer(data=request.data)
        if serializer.is_valid():
            tmdb_id = serializer.validated_data['tmdb_id']
            history, created = WatchHistory.objects.get_or_create(
                user=request.user,
                tmdb_id=tmdb_id
            )
            if created:
                return Response({"status": "added"}, status=201)
            return Response({"status": "already exists"}, status=200)
        return Response(serializer.errors, status=400)
    
class WatchHistoryRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tmdb_id):
        deleted, _ = WatchHistory.objects.filter(user=request.user, tmdb_id=tmdb_id).delete()
        if deleted:
            return Response({"status": "removed"})
        return Response({"status": "not found"}, status=404)
    
class FavoriteCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tmdb_id):
        exists = FavoriteMovie.objects.filter(user=request.user, tmdb_id=tmdb_id).exists()
        return Response({ "liked": exists })

class FavoriteAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WatchHistorySerializer(data=request.data)
        if serializer.is_valid():
            tmdb_id = serializer.validated_data['tmdb_id']
            _, created = FavoriteMovie.objects.get_or_create(user=request.user, tmdb_id=tmdb_id)
            return Response({ "status": "added" if created else "exists" })
        return Response(serializer.errors, status=400)

class FavoriteRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tmdb_id):
        deleted, _ = FavoriteMovie.objects.filter(user=request.user, tmdb_id=tmdb_id).delete()
        return Response({ "status": "removed" if deleted else "not found" })

