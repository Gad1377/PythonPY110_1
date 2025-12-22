from django.shortcuts import render
import  random
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from app_store.logic.services import filtering_category
from .logic.control_cart import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render

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
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse").lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data, 'category': category_key})

# def
def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    data_other_products = [prod for prod in DATABASE.values() if
                                           prod['category'] == data['category'] and prod['name'] != data['name']]
                    if len(data_other_products) > 5:
                        data_other_products = random.sample(data_other_products, k=5)
                    return render(request, 'app_store/product.html', context={'product': data,
                                                                              'other_products': data_other_products})

        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                data_other_products = [prod for prod in DATABASE.values() if
                                       prod['category'] == data['category'] and prod['name'] != data['name']]
                if len(data_other_products) > 5:
                    data_other_products = random.sample(data_other_products, k=5)
                return render(request, 'app_store/product.html', context={'product': data,
                                                                          'other_products': data_other_products})




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

def cart_view(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username)[username]  # Получаем корзину пользователя username

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # Получаем информацию о продукте
            # TODO в словарь product под ключом "quantity" запишите текущее значение количества товара в корзине
            product["quantity"] = quantity  # Реализуйте
            # TODO в словарь product под ключом "price_total" посчитайте и запишите общую стоимость товара как произведение
            #  его количества в корзине на цену с учетом скидки ('price_after'). Значение цены "price_total" приведите к формату
            #  2 символов после запятой
            product["price_total"] = product['price_after'] * quantity  # Реализуйте
            # TODO добавьте словарь product в конец списка products
            # Реализуйте
            products.append(product)
        return render(request, "app_store/cart.html", context={'products':products})