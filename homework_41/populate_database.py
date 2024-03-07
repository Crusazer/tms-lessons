import json

from models import Product, Category, create_database_session

session = create_database_session()


def populate_database(path: str = 'data.json'):
    session.query(Product).delete()
    session.query(Category).delete()
    with open('data.json', 'r') as file:
        data_list = json.load(file)

        for data in data_list:
            category = Category(name=data.get('name'))
            for product_data in data.get('products'):
                product = Product(name=product_data['name'], description=product_data['description'],
                                  price=product_data['price'])
                category.products.append(product)
            session.add(category)
            session.commit()


def print_all_question_with_choices() -> None:
    categories = session.query(Category).all()
    for category in categories:
        products = ', '.join(
            f"{product.name}__({product.description})__{product.price}" for product in category.products)
        print(f"{category.name}: {products}")


if __name__ == "__main__":
    populate_database()
    print_all_question_with_choices()
