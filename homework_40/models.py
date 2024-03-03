from pydantic import BaseModel


class User(BaseModel):
    user_id: int = 0
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    password2: str


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: int


class Category(BaseModel):
    id: int
    name: str
    products: list[Product] | None = None


class PaginationBase(BaseModel):
    count: int = 0
    previous: int | None = None
    next: int | None = None

    def paginate(self, page_size: int, page: int):
        count_page: int = self.count // page_size
        if self.count % page_size > 0:
            count_page += 1
        self.previous: int = page - 1 if page - 1 > 0 else None
        self.next: int = page + 1 if page + 1 <= count_page else None


class ProductsPaginated(PaginationBase):
    results: list[Product]


class CategoryPaginated(PaginationBase):
    results: list[Category]


class Database:
    def __init__(self):
        self._users: list[User] = []
        self._categories: list[Category] = self._generate_fake_categories()
        self._products: list[Product] = [product for category in self._categories for product in category.products]

    def _generate_fake_categories(self):
        categories = [
            Category(
                id=1,
                name="Electronics",
                products=[
                    Product(id=1, name="iPhone 13", description="The latest iPhone from Apple.", price=999, category=1),
                    Product(id=2, name="Samsung Galaxy S22", description="The latest Samsung Galaxy phone.", price=899,
                            category=1),
                ],
            ),
            Category(
                id=2,
                name="Clothing",
                products=[
                    Product(id=3, name="T-shirt", description="A basic T-shirt.", price=19.99, category=2),
                    Product(id=4, name="Jeans", description="A pair of jeans.", price=49.99, category=2),
                ],
            ),
            Category(
                id=3,
                name="Home Goods",
                products=[
                    Product(id=5, name="Couch", description="A comfortable couch.", price=999, category=3),
                    Product(id=6, name="Table", description="A sturdy table.", price=299, category=3),
                ],
            ),
            Category(
                id=4,
                name="Food",
                products=[
                    Product(id=7, name="Pizza", description="A delicious pizza.", price=14.99, category=4),
                    Product(id=8, name="Burger", description="A juicy burger.", price=9.99, category=4),
                ],
            ),
            Category(
                id=5,
                name="Other",
                products=[
                    Product(id=9, name="Book", description="A good book.", price=19.99, category=5),
                    Product(id=10, name="Movie ticket", description="A ticket to the latest movie.", price=12.99,
                            category=5),
                ],
            ),
        ]
        return categories

    def register_user(self, user: User) -> User | None:
        if user.password != user.password2:
            return None

        if self._users:
            user.user_id = self._users[-1].user_id + 1
        else:
            user.user_id = 1
        self._users.append(user)
        return user

    def get_category(self, category_id: int) -> Category | None:
        for category in self._categories:
            if category_id == category.id:
                return category

        return None

    def get_product(self, product_id) -> Product | None:
        for product in self._products:
            if product_id == product.id:
                return product

        return None

    def get_products_from_category(self, category_id: int) -> list[Product] | None:
        category: Category = self.get_category(category_id)
        if category is None:
            return None

        return category.products

    def get_categories(self):
        return self._categories
