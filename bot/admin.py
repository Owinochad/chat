from django.contrib import admin
from .models import Image, ChatMessage, FeedBack

# Register your models here.

admin.site.register(Image)
admin.site.register(ChatMessage)
@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display=('name','email')
