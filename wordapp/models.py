from django.db import models


# Create your models here.
class WordTable(models.Model):
    word = models.CharField(max_length=100)
    trans = models.CharField(max_length=200)
    use_num = models.IntegerField(default=0)

    def __str__(self):
        return self.word