from django.shortcuts import render

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from app_store.logic.services import filtering_category
from .logic.control_cart import view_in_cart, add_to_cart, remove_from_cart

def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE.get(id_), json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            else:
                return HttpResponseNotFound('Данного продукта нет в базе данных!')
        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            reverse = request.GET.get('reverse')
            if reverse and reverse.lower() == 'true':
                data = filtering_category(DATABASE,category_key,ordering_key,True)
            else:
                data = filtering_category(DATABASE,category_key,ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

    return JsonResponse(data, safe=False,  json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)

def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
            for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
                    with open(f'app_store/product/{page}.html', encoding='utf-8') as f:
                        s = f.read()
                        return HttpResponse(s)

            return HttpResponse(status=404)

        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'app_store/product/{data["html"]}.html', encoding='utf-8') as f:
                    return HttpResponse(f.read())
            return HttpResponse(status=404)

def cart_view_json(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username=username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = add_to_cart(id_product, username=username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})