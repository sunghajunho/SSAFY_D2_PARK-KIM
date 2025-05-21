from rest_framework import status, viewsets, generics, permissions, serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from .models import Follow
from .serializers import (
    SignupSerializer, LoginSerializer, UserSerializer, ChangePasswordSerializer,
    FollowSerializer, UserProfileSerializer
)

User = get_user_model()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.context['user']
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def logout_view(request):
    logout(request)
    return Response(status=204)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def withdraw(request):
    request.user.delete()
    return Response(status=204)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def update(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    user = request.user
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': ['Wrong password']}, status=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        return Response({'message': 'Password changed successfully'})
    return Response(serializer.errors, status=400)

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def perform_create(self, serializer):
        following_id = self.request.data.get('following')
        if following_id == str(self.request.user.id):
            raise serializers.ValidationError("자기 자신을 팔로우할 수 없습니다.")
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        following_id = request.data.get('following')
        try:
            following_user = User.objects.get(id=following_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'})
        return Response({'status': 'followed'})
