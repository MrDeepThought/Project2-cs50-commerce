from django.urls import path, reverse

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/<str:username>", views.create_listing, name="create"),
    path("lisitng/<str:username>/<int:listingId>", views.listing, name="listing"),
    path("categories/<str:categoryName>", views.category_listings, name="categoryListings"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("categories", views.categories_page, name="categories"),
    path('login', views.login_view, name="login"),
]
