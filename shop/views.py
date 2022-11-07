from django.shortcuts import render
from .models import Product, Contact
from math import ceil
from django.http import HttpResponse


# Create your views here.
def index(request):
    products = Product.objects.all()
    # print(products)
    # n = len(products)
    # slides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides': slides, 'range': range(1,  slides), 'product': products}
    # Prod = [[products, range(1, slides), slides], [products, range(1, slides), slides]]
    Prod = []
    catProd = Product.objects.values('product_category', 'product_id')
    cats = {item['product_category'] for item in catProd}
    for cat in cats:
        Proddd = Product.objects.filter(product_category=cat)
        n = len(Proddd)
        slides = n // 4 + ceil((n / 4) - (n // 4))
        Prod.append([Proddd, range(1, slides), slides])
    params = {'Produ': Prod}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def search(request):
    return render(request, 'shop/search.html')


def tracker(request):
    return render(request, 'shop/tracker.html')


def produ(request, my):
    product = Product.objects.filter(product_id=my)
    print(product)
    return render(request, 'shop/products.html', {'product': product[0]})
    # return render(request, 'shop/products.html')


def checkout(request):

    return render(request, 'shop/checkout.html', )
