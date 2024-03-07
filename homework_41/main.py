from typing import Type

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from serializers import paginate, serialize_category
from models_scheme import UserScheme, ProductsPaginatedScheme, ProductScheme, CategoryScheme, CategoryPaginatedScheme
from serializers import serialize_user, serialize_product
from models import create_database_session, User, Product, Category

session = create_database_session()
app = FastAPI()


class Message(BaseModel):
    detail: str


@app.post('/register/', responses={400: {"model": Message, "description": "Incorrect password"}})
async def register(user_scheme: UserScheme) -> UserScheme:
    if user_scheme.password != user_scheme.password2 or user_scheme.password is None:
        raise HTTPException(status_code=400, detail='Incorrect password')

    user_db = User(first_name=user_scheme.first_name, last_name=user_scheme.last_name, email=user_scheme.email,
                   username=user_scheme.username, password=user_scheme.password)
    session.add(user_db)
    session.commit()

    return serialize_user(user_db)


@app.get('/products/', responses={400: {"model": Message, "description": 'Incorrect page number'},
                                  404: {'model': Message, 'description': 'Product not fount'}})
async def get_products(category_id: int, page_size: int = 5, page: int = 1) -> (ProductsPaginatedScheme |
                                                                                Type[ProductsPaginatedScheme]):
    if page < 1:
        raise HTTPException(status_code=400, detail=f"Page can't be less then 1, but you send {page}")

    products_db = session.query(Product).filter(Product.category_id == category_id).offset(
        (page - 1) * page_size).limit(page_size).all()

    if not products_db:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not founded")

    products_scheme = [serialize_product(product) for product in products_db]

    total_count = session.query(Product).filter(Product.category_id == category_id).count()
    return paginate(ProductsPaginatedScheme, products_scheme, page_size, page, total_count)


@app.get('/products/{product_id}/', responses={404: {'model': Message, 'description': 'Product not found'}})
async def get_product(product_id: int) -> ProductScheme:
    product_db = session.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not founded")
    return serialize_product(product_db)


@app.get('/categories/', responses={400: {'model': Message, 'description': 'Incorrect page number'},
                                    404: {'model': Message, 'description': 'Category not found'}})
async def get_categories(page_size: int = 5, page: int = 1, include_products: bool = True) -> (
        CategoryPaginatedScheme | Type[CategoryPaginatedScheme]):
    if page < 1:
        raise HTTPException(status_code=400, detail=f"Page can't be less then 1, but you send {page}")

    categories_db = session.query(Category).order_by(Category.id).offset((page - 1) * page_size).limit(page_size).all()

    if not categories_db:
        raise HTTPException(status_code=404, detail=f"Categories not founded")

    categories_scheme: list[CategoryScheme] = [serialize_category(category, include_products) for category in
                                               categories_db]
    total_count = session.query(Category).count()
    return paginate(CategoryPaginatedScheme, categories_scheme, page_size, page, total_count)


@app.get('/categories/{category_id}/', responses={404: {'model': Message, 'description': 'Category not found'}})
async def get_category(category_id: int, include_products: bool = True) -> CategoryScheme:
    category_db = session.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not founded")

    return serialize_category(category_db, include_products)
