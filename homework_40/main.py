import copy

from fastapi import FastAPI, HTTPException
from models import Database, User, Product, Category, ProductsPaginated, CategoryPaginated

app = FastAPI()
db = Database()


@app.post('/register/')
async def register(user: User) -> User:
    user = db.register_user(user)
    if user is None:
        HTTPException(status_code=400, detail="Incorrect data")
    return user


@app.get('/products/')
async def get_products(category_id: int, page_size: int = 5, page: int = 1) -> ProductsPaginated:
    products: list[Product] = db.get_products_from_category(category_id)
    if products is None:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not founded")

    paginated_products = ProductsPaginated(count=len(products),
                                           results=products[(page - 1) * page_size:page * page_size])
    paginated_products.paginate(page_size, page)
    return paginated_products


@app.get('/products/{product_id}/')
async def get_product(product_id: int) -> Product:
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=400, detail=f"Product with id {product_id} not founded")
    return product


@app.get('/categories/')
async def get_categories(page_size: int = 5, page: int = 1, include_products: bool = True):
    categories: list[Category] = copy.deepcopy(db.get_categories())

    if not categories:
        return categories

    if include_products is False:
        for category in categories:
            category.products = None

    paginated_categories = CategoryPaginated(count=len(categories),
                                             results=categories[(page - 1) * page_size: page * page_size])
    paginated_categories.paginate(page_size, page)
    return paginated_categories


@app.get('/categories/{category_id}/')
async def get_category(category_id: int, include_products: bool = True) -> Category:
    category: Category = copy.deepcopy(db.get_category(category_id))
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not founded")

    if include_products is False:
        category.products = None

    return category
