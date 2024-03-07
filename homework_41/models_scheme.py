from pydantic import BaseModel


class UserScheme(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: str
    username: str
    password: str | None = None
    password2: str | None = None


class ProductScheme(BaseModel):
    id: int
    name: str
    description: str
    price: int
    category: int


class CategoryScheme(BaseModel):
    id: int
    name: str
    products: list[ProductScheme] | None = None


class PaginationBaseScheme(BaseModel):
    count: int = 0
    previous: int | None = None
    next: int | None = None


class ProductsPaginatedScheme(PaginationBaseScheme):
    results: list[ProductScheme]


class CategoryPaginatedScheme(PaginationBaseScheme):
    results: list[CategoryScheme]
