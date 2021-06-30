from django.contrib import admin

from foodlink_back.apps.authentication.models import CoreUser, UserOtp, PhoneNumber

admin.site.register(CoreUser)
admin.site.register(UserOtp)
admin.site.register(PhoneNumber)
