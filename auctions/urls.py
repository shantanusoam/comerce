from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_list, name="create_list"),
    path("<str:title>", views.description, name="description"),
    path("addwishlist", views.addwishlist, name="addwishlist"),
    path('delete/<int:desc_id>', views.deletelist, name="deletelist")
]
