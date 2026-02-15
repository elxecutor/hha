from django.db import models

class Hymn(models.Model):
    title = models.CharField(max_length=200, unique=True)
    lyrics = models.TextField(help_text="Hymn lyrics, with each line separated by newlines")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']