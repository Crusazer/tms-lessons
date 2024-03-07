from typing import Any, Type, TypeVar

import math

from models import User, Product, Category
from models_scheme import UserScheme, ProductScheme, CategoryScheme

T = TypeVar('T')


def serialize_user(user: User) -> UserScheme:
    return UserScheme(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email,
                      username=user.username)


def serialize_product(product: Product | Type[Product]) -> ProductScheme:
    return ProductScheme(id=product.id, name=product.name, description=product.description, price=product.price,
                         category=product.category_id)


def serialize_category(category: Category | Type[Category], include_products: bool = True) -> CategoryScheme:
    if include_products:
        return CategoryScheme(id=category.id, name=category.name,
                              products=[serialize_product(product) for product in category.products])
    return CategoryScheme(id=category.id, name=category.name)


def paginate(model: T, list_scheme: list[Any], page_size: int, page: int, total_count: int) -> T:
    count = len(list_scheme)
    count_page: int = math.ceil(total_count / page_size)
    previous_page: int = page - 1 if page - 1 > 0 else None
    next_page: int = page + 1 if page + 1 <= count_page else None
    return model(count=count, previous=previous_page, next=next_page, results=list_scheme)
