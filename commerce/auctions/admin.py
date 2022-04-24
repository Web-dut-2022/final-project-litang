from django.contrib import admin

from .models import *

class ListAdmin(admin.ModelAdmin):
    list_display = ("__str__")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("__str__")

admin.site.register(List)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(User)
