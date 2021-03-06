from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("myitem", views.myitem, name="myitem"),
    path("gotit", views.gotit, name="gotit"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_item>", views.listing, name="listing"),
    path("bid/<str:listing_item>", views.bid, name="bid"),
    path("close/<str:listing_item>", views.close, name="close"),
    path("watch/<str:listing_item>", views.watch, name="watch"),
    path("watch_open", views.watch_open, name="watch_open"),
    path("delete/<int:listing_item>", views.delete, name="delete"),
    path("add_comment/<str:listing_item>", views.add_comment, name="add_comment"),
    path("category", views.category, name="category"),
    path("onecategory/<str:listing_item>", views.onecategory, name="onecategory"),
    path("search", views.search, name="search"),
    path('admin/', admin.site.urls),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
