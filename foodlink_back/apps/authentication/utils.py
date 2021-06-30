from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler


class Pagination(object):
    @classmethod
    def number_of_pages(cls, num_of_instances, instances_per_page=12):
        num_of_pages = (
            (num_of_instances // instances_per_page)
            if num_of_instances % instances_per_page == 0
            else (num_of_instances // instances_per_page) + 1
        )
        return num_of_pages


class CustomDefaultPagination(PageNumberPagination, Pagination):
    page_size = 12

    def get_paginated_response(self, data, *args, **kwargs):
        num_of_instances = self.page.paginator.count
        return Response(
            {
                'data': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'page': self.number_of_pages(
                        self.page.paginator.count, self.page_size
                    ),
                    'per_page': self.page_size,
                    'current_page': self.page.number,
                    'total': num_of_instances,
                    'data': data,
                }
            }
        )


def custom_jwt_create_payload(user):
    payload = jwt_payload_handler(user)
    if not payload.get('user_id', None):
        payload['user_id'] = user.id
    if not payload.get('phone', None):
        payload['phone'] = user.phone
    payload['first_name'] = user.first_name
    payload['last_name'] = user.last_name
    return payload
