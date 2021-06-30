from enum import Enum


class PaymentMethods(Enum):
    ONLINE = "ONLINE"
    CASH = "CASH"


class PaymentInterface:
    choices = (
        (PaymentMethods.ONLINE.name, PaymentMethods.ONLINE.value),
        (PaymentMethods.CASH.name, PaymentMethods.CASH.value),
    )
