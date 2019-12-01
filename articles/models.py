from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk', )


class Comment(models.Model): # Article 과 1:N 관계
    article = models.ForeignKey(
        Article,
        on_delete="models.CASCADE",
        related_name="comments",
        )
    content = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    # user : comment = 1 : N 관계
    # --> c.user (1명) 으로 접근 / u.comment_set.all() 에서 이름 설정 --> u.comments.all() 로 
    
    class Meta:
        ordering = ['-pk']
