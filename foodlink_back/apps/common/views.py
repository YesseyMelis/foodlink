import logging

from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodlink_back.apps.authentication.serializers import ErrorResponseSerializer
from foodlink_back.apps.common.models import Product
from foodlink_back.apps.common.serializers import ProductSerializer
from foodlink_back.apps.common.services import make_menu_from_product

logger = logging.getLogger(__name__)


class ProductAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser)

    def create(self, request, *args, **kwargs):
        cook = request.user
        if cook.is_cook:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                logger.info('User {} created a product {}'.format(cook, product))
                make_menu_from_product(product=product, cook=cook)
                return Response(serializer.data)
            else:
                logger.error('Product create serializer validation error.')
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        ser = ErrorResponseSerializer(data={'error': 'User is not cooker.'})
        ser.is_valid(raise_exception=True)
        return Response(ser.data, status=status.HTTP_400_BAD_REQUEST)
