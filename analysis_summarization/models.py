from django.db import models

# Create your models here.
class search(models.Model):
    tweet_tag = models.CharField(max_length = 30)
    analysis_tweets = models.CharField(max_length = 3000)
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.tweet_tag
