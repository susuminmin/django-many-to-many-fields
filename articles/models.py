from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    
    class Meta:
        ordering = ['-pk']
