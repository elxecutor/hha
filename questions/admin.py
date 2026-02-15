from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question_text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('question_text',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def question_text_short(self, obj):
        """Display shortened question text in list view"""
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = "Question"
