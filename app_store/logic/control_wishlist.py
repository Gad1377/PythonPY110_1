import json
import os

PATH_WISHLIST = 'wishlist.json'  # Путь до файла избранного


def view_in_wishlist(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое wishlist.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}  # Пустое избранное для пользователя

    if os.path.exists(PATH_WISHLIST):  # Если файл с избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем избранное
            if username not in wishlist:  # Если пользователя нет в избранном, то создаем запись с пустым избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с избранным нет
        wishlist = {username: empty_user_wishlist}

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем избранное
        json.dump(wishlist, f)

    return wishlist  # Возвращаем содержимое избранного


def add_to_wishlist(id_product: str, username: str = ''):
    wishlist = view_in_wishlist(username)
    if id_product not in wishlist[username]['products']:
        wishlist[username]['products'].append(id_product)
        with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
            json.dump(wishlist, f)
        return True
    return False


def remove_from_wishlist(id_product: str, username: str = ''):
    wishlist = view_in_wishlist(username)
    if id_product in wishlist[username]['products']:
        wishlist[username]['products'].remove(id_product)
        with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
            json.dump(wishlist, f)
        return True
    return False
