
from django.urls import path
from.import views
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/",views.tracker, name="Tracker"),
    path("search/", views.search, name="Search"),
    path("products/<int:my>", views.produ, name="Produ"),
    path("checkout/", views.checkout, name="Checkout"),
]