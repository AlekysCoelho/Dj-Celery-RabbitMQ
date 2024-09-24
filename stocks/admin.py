from django.contrib import admin

from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "ticker",
        "current_price",
        "moment",
    )
    search_fields = ("ticker",)
    list_filter = ("ticker",)
