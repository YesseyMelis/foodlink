from foodlink_back.apps.authentication.models import CoreUser
from foodlink_back.apps.common.models import Product, CookMenu


def make_menu_from_product(
        *,
        product: Product,
        cook: CoreUser
):
    if cook.menu.exists():
        menu = cook.menu.first()
        menu.foods.add(product)
    else:
        menu = CookMenu.objects.create(cook=cook)
        menu.foods.add(product)
    return menu
