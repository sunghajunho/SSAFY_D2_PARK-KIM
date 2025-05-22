from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import CustomUserSerializer, FollowSerializer
from .models import CustomUser, Follow
from core.models import Genre
from rest_framework import status, viewsets, generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
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
        try:
            following_user = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'})
        return Response({'status': 'followed'})


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all().values('id', 'name')
        return Response(genres)