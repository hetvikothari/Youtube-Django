from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    published_date = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=2000)  
    video_id = models.CharField(max_length=200)

    def __str__(self):  
        return f'{self.title}'