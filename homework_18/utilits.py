""" This file contains functions for create html strings. And some other functions. """
from flask import session
from homework_18.db import Product


def get_main_page_string(data: list) -> str:
    string = '<ul>'
    category = ''
    fist_step_flag = True

    for product in data:
        if category != product[4]:  # 4 is product.name in tuple
            category = product[4]

            if fist_step_flag:
                fist_step_flag = False
            else:
                string += f'</ul></li>'
            # 3 is category_id
            string += f'''\n<br><li><a href="http://127.0.0.1:8080/category/{product[3]}">{category}<a><ul>'''
            string += f"\n<li>{product[1]}</li>"  # 1 is product.name in tuple
        else:
            string += f"\n<li>{product[1]}</li>"
    string += '</ul>'
    return string


def get_product_string(product: Product) -> str:
    sign = ''
    text_button = "Добавить в избранное"
    if session.get('is_authenticated') and product.id in session.get('favorite_products_id'):
        sign = '&#10027;'
        text_button = "Удалить из избранного"

    return f'''<b><ul>
                    <a href="http://127.0.0.1:8080/product/{product.id}">{product.name} {sign}</a>
                </ul></b>
               Описание: {product.description}
               <form action="/add_favorite/{product.id}" method="post">        
                    <input type="submit" value="{text_button}"><br>
               </form>     
            '''


def get_authentication_string(additional_data: str = '', username: str = '', password: str = ''):
    return f'''
                <body>
                    <h1 style="text-align: center;">Авторизация пользователя</h1>
                    <form action="/auth" method="post">
                        {additional_data}<br>
                        Логин:    <input type="text" name="username" value="{username}"/><br>
                        Пароль: <input type="password" name="password" value="{password}"/><br>
                        <input type="submit" value="Войти"><br>
                        <a href="http://127.0.0.1:8080/registration">Зарегистрироваться</a><br>     
                        <a href="http://127.0.0.1:8080/">На главную страницу</a>                             
                    </form>
                </body>
            '''


def get_registration_string(additional_data: str = '', username: str = '', password: str = ''):
    return f'''
                    <h1 style="text-align: center;">Регистрация пользователя</h1>
                    <form action="/registration" method="post">
                        {additional_data}<br>
                        Логин:    <input type="text" name="username" value="{username}"/><br>
                        Пароль: <input type="password" name="password" value="{password}"/><br>
                        <input type="submit" value="Зарегистрироваться"><br>
                        <a href="http://127.0.0.1:8080/auth">Вход в аккаунт</a><br>
                        <a href="http://127.0.0.1:8080/">На главную страницу</a>                                   
                    </form>
            '''


def get_upper_string():
    if session.get("is_authenticated"):
        string = f'''{session.get("username")}<br>
                    <a href="http://127.0.0.1:8080/favorites">Любимые товары</a> &emsp;
                    <a href="http://127.0.0.1:8080/">Вернуться на главную страницу</a>
                    <form action="/logout" method="post">
                        <input type="submit" value="Выйти из аккаунта"><br>
                    </form>
                    <hr> 
                '''
    else:
        string = f'''
                    <a href="http://127.0.0.1:8080/auth">Войти в аккаунт</a> &emsp;
                    <a href="http://127.0.0.1:8080/">Вернуться на главную страницу</a><hr>
                  '''

    return string
