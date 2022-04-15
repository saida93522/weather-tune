from django.db import models

# Create your models here.
class SpotifyProfile(models.Model):
    username = models.CharField(max_length=200,blank=False,null=False)

    def __str__(self):
        return self.username
    