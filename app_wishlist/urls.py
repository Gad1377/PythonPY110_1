from django.urls import path

from app_wishlist.views import wishlist_view, wishlist_view_json, wishlist_add_view_json, wishlist_del_view_json, wishlist_remove_view

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name="wishlist_view"),
    path('api/', wishlist_view_json, name="wishlist_api"),
    path('api/add/<str:id_product>', wishlist_add_view_json, name="wishlist_add_api"),
    path('api/del/<str:id_product>', wishlist_del_view_json, name="wishlist_del_api"),
    path('remove/<str:id_product>', wishlist_remove_view, name="wishlist_remove_view")
]
