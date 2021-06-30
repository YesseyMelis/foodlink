from django.contrib import admin

from foodlink_back.apps.common.models import Product, CookMenu, CookRating

admin.site.register(Product)
admin.site.register(CookMenu)
admin.site.register(CookRating)
