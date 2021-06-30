from foodlink_back.apps.order.enums import Statuses


class OrderStatuses:
    choices = (
        (Statuses.COLLECTION.value, Statuses.COLLECTION.name),
        (Statuses.COOKING.value, Statuses.COOKING.name),
        (Statuses.ASSEMBLY.value, Statuses.ASSEMBLY.name),
        (Statuses.DELIVERY.value, Statuses.DELIVERY.name)
    )
