from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create", views.create_listing, name="create"),
    path("whatchlist", views.watchlist, name="watchlist"),
    path("addwhatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path('removewatchlist/<int:id>/', views.removewatchlist, name='removewatchlist'),
    path("categorys", views.categorys, name="categorys"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("comment/<int:id>", views.comment, name="comment"),
    path('showcategory/', views.showCategory, name='showcategory'),
    path("bid/<int:id>", views.bid, name="bid"),
    path("closeAuc/<int:id>", views.closeAuc, name="closeAuc"),

]
