from django.urls import path

from foodlink_back.apps.common.views import ProductAPIView

urlpatterns = [
    path('product/create/', ProductAPIView.as_view(), name='product-create'),
]

app_name = 'common'
