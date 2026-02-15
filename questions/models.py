from django.db import models


class Question(models.Model):
    question_text = models.TextField(help_text="The question being asked")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.question_text[:50] + "..." if len(self.question_text) > 50 else self.question_text
