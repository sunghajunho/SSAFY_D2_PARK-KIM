from rest_framework import serializers

class RecommendationRequestSerializer(serializers.Serializer):
    input = serializers.CharField(required=True, help_text="사용자의 취향이나 요청 문장")

class MovieInfoSerializer(serializers.Serializer):
    title = serializers.CharField()
    overview = serializers.CharField()
    poster_path = serializers.CharField(allow_null=True, required=False)
    release_date = serializers.CharField(allow_null=True, required=False)
    vote_average = serializers.FloatField(allow_null=True, required=False)

class RecommendationResponseSerializer(serializers.Serializer):
    results = MovieInfoSerializer(many=True)
