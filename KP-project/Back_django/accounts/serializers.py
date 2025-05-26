from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import CustomUser, UserGenrePreference, Follow
from core.models import Genre

class CustomRegisterSerializer(RegisterSerializer):
    real_name = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(choices=CustomUser._meta.get_field('gender').choices, required=True)
    mbti = serializers.ChoiceField(choices=CustomUser._meta.get_field('mbti').choices, required=True)
    region = serializers.ChoiceField(choices=CustomUser._meta.get_field('region').choices, required=True)
    # 장르 우선순위 (예: 1~3순위)
    preferred_genres = serializers.ListField(child=serializers.IntegerField(), required=True)
    
    class Meta:
        fields = [
            'username', 'email', 'password1', 'password2',
            'real_name', 'nickname', 'age', 'gender', 'mbti', 'region', 'preferred_genres'
        ]

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        extra_fields = ['real_name', 'nickname', 'age', 'gender', 'mbti', 'region', 'preferred_genres']
        for field in extra_fields:
            data[field] = self.validated_data.get(field)
        return data

    def save(self, request):
        user = super().save(request)
        user.real_name = self.cleaned_data.get('real_name')
        user.nickname = self.cleaned_data.get('nickname')
        user.age = self.cleaned_data.get('age')
        user.gender = self.cleaned_data.get('gender')
        user.mbti = self.cleaned_data.get('mbti')
        user.region = self.cleaned_data.get('region')
        user.save()

        preferred_genres = self.cleaned_data.get('preferred_genres')
        if preferred_genres:
            for i, genre_id in enumerate(preferred_genres):
                genre = Genre.objects.get(id=genre_id)
                UserGenrePreference.objects.create(user=user, genre=genre, priority=i+1)

        return user

class CustomUserSerializer(serializers.ModelSerializer):
    preferred_genres = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'real_name', 'age', 'gender', 'mbti', 'region', 'preferred_genres']

    def get_preferred_genres(self, user):
        return [
            {
                "id": pref.genre.id,
                "name": pref.genre.name,
                "priority": pref.priority
            }
            for pref in user.genre_preferences.all().order_by('priority')
        ]
    
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['follower']

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = CustomUser
        fields = (
            'id', 'username', 'email',
            'real_name', 'nickname', 'age',
            'gender', 'mbti', 'region'
        )
        
class WatchHistorySerializer(serializers.Serializer):
    tmdb_id = serializers.IntegerField()
