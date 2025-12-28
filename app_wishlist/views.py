from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from django.contrib.auth import get_user
from app_store.logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth.decorators import login_required

# def wishlist_view(request):
#     if request.method == "GET":
#         if request.method == "GET":
#             return render(request, "app_wishlist/wishlist.html")

def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)

        products = []
        for product_id in data.get(username, {}).get('products', []):
            product_data = DATABASE.get(product_id, {})
            if product_data:
                products.append(product_data)

        return render(request, 'app_wishlist/wishlist.html', context={"products": products})



@login_required(login_url='app_login:login_view')
def wishlist_view_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        username = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(username=username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


@login_required(login_url='app_login:login_view')
def wishlist_add_view_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_wishlist(id_product=id_product, username=username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"}, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404, json_dumps_params={'ensure_ascii': False})


@login_required(login_url='app_login:login_view')
def wishlist_del_view_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product=id_product, username=username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"}, json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404, json_dumps_params={'ensure_ascii': False})

@login_required(login_url='app_login:login_view')
def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product, username)
        if result:
            return redirect("app_wishlist:wishlist_view")
        return HttpResponseNotFound("Неудачное удаление из избранного")

