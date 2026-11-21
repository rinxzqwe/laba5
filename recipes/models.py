from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cooking_time = models.IntegerField()
    ingredients = models.TextField()
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'author', 'category', 'cooking_time', 'ingredients')