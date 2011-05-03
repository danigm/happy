from django.contrib import admin
from models import Happy, Advise


class HappyAdmin(admin.ModelAdmin):
    list_display = ('happy', 'day', 'reason')


class AdviseAdmin(admin.ModelAdmin):
    list_display = ('happy', 'ad', 'votes')


admin.site.register(Happy, HappyAdmin)
admin.site.register(Advise, AdviseAdmin)
