from django.db import models

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True) 

class ChatMessage(models.Model):
    prompt = models.CharField(max_length=255)
    response = models.TextField()


class FeedBack(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    feedback=models.TextField()
 
