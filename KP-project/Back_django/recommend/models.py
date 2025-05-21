from django.db import models
from django.conf import settings

class RecommendationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_text = models.TextField()
    gpt_prompt = models.TextField()
    gpt_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)