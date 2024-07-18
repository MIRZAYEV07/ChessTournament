from django.contrib import admin

from user.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "rating", "country", "points")
    search_fields = ("name", "country")
    list_filter = ("country",)


admin.site.register(Player, PlayerAdmin)
