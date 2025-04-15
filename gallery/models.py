from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='favorite_images', blank=True)

    # def __str__(self):
    #     return self.title
    

    def total_likes(self):
        return self.liked_by.count()
    




class Comment(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.text[:20]}"
