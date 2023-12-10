""" This file contains functions for working with the database. """
import dataclasses
import sqlite3

from shop import DATABASE_PATH


@dataclasses.dataclass
class Product:
    id: int
    name: str
    description: str
    category_id: int


@dataclasses.dataclass
class Category:
    id: int
    name: str


@dataclasses.dataclass
class User:
    user_id: int
    username: str
    password: str


def load_products() -> list[Product]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        all_products = connection.execute("SELECT * FROM product")
        return [Product(*product) for product in all_products.fetchall()]


def load_product(product_id: int) -> Product:
    assert type(product_id) is int, "Incorrect product id in func::Load_product."

    with sqlite3.connect(DATABASE_PATH) as connection:
        execute_product = connection.execute("SELECT * FROM product WHERE id = ?", (product_id,))

        if product := execute_product.fetchone():
            return Product(*product)
        else:
            raise ValueError("Product not found")


def load_products_from_category(category_id: int) -> list[Product]:
    assert type(category_id) is int, "Incorrect product id in func::load_products_from_category."

    with sqlite3.connect(DATABASE_PATH) as connection:
        products_execute = connection.execute('''SELECT product.id, product.name, description, category_id
                                              FROM product
                                              WHERE category_id = ?''', (category_id,))
        return [Product(*product) for product in products_execute.fetchall()]


def load_product_order_by_categories() -> list:
    """ Return list(product_id, product_name, description, category_id, category.name"""
    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute('''SELECT product.id, product.name, description, category_id, category.name
                                              FROM product INNER JOIN category ON product.category_id == category.id
                                              ORDER BY category.id''')
        return execute.fetchall()


def load_user(username: str) -> User:
    assert username is not str, "Incorrect value in func::load_user."

    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute("SELECT * FROM user WHERE name = ?", (username,))
    user = execute.fetchone()
    return User(*user) if user else None


def create_user(username: str, password: str):
    assert username is not str, "Incorrect value in func::load_user."
    assert password is not str, "Incorrect value in func::load_user."

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("INSERT INTO user (name, password) VALUES (?, ?)", (username, password))


def load_favorites_user_products_id(user_id: int) -> list[int]:
    assert user_id is not int, "Incorrect value in func::load_user."

    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute(f"SELECT product_id FROM user_to_product WHERE user_id = ?", (user_id,))
        products = execute.fetchall()
        return [i[0] for i in products] if products else []


def add_favorite_product(user_id: int, product_id: int):
    assert user_id is not int, "Incorrect value in func::load_user."
    assert product_id is not int, "Incorrect value in func::load_user."

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("INSERT INTO user_to_product VALUES(?, ?)", (user_id, product_id))


def delete_favorite_product(user_id: int, product_id: int):
    assert user_id is not int, "Incorrect value in func::load_user."
    assert product_id is not int, "Incorrect value in func::load_user."

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("DELETE FROM user_to_product WHERE user_id = ? AND product_id = ?", (user_id, product_id))


def load_category_name(category_id: int):
    assert category_id is not int, "Incorrect value in func::load_category_name"

    with sqlite3.connect(DATABASE_PATH) as connection:
        execute = connection.execute("SELECT name FROM category WHERE id = ?", (category_id,))
    return execute.fetchone()[0]
