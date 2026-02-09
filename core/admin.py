from django.contrib import admin
from .models import Leader, Worker
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'get_contact_link')
    list_filter = ('name',)
    search_fields = ('name', 'phone_number')
    ordering = ('name',)
    list_per_page = 25

    def get_contact_link(self, obj):
        return format_html('<a href="tel:{}" class="button">📞 Call</a>', obj.phone_number)
    get_contact_link.short_description = 'Contact'


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'get_contact_link')
    list_filter = ('name',)
    search_fields = ('name', 'phone_number')
    ordering = ('name',)
    list_per_page = 25

    def get_contact_link(self, obj):
        return format_html('<a href="tel:{}" class="button">📞 Call</a>', obj.phone_number)
    get_contact_link.short_description = 'Contact'
