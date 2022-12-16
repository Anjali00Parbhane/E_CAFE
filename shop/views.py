from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.http import HttpResponse
import json
# from django.views.decorators.csrf import csrf_exempt
# from .import Checksum
# from paytmchecksum import PaytmChecksum
# import requests
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'Your-Merchant-Key-Here'


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
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def produ(request, my):
    product = Product.objects.filter(product_id=my)
    print(product)
    return render(request, 'shop/products.html', {'product': product[0]})
    # return render(request, 'shop/products.html')


def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(item_json=item_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc='The order has been placed')
        update.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        # param_dict = {
        #
        #     'MID': 'Your-Merchant-Id-Here',
        #     'ORDER_ID': str(order.order_id),
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        #
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        #
        # paytmParams = dict()
        #
        # paytmParams["body"] = {
        #     "requestType": "Payment",
        #     "mid"        : Paytm_id,
        #     "websiteName": "YOUR_WEBSITE_NAME",
        #     "orderId"    : str(order.order_id),
        #     "callbackUrl": "http://127.0.0.1:8000/shop/handlerequest/",
        #     "txnAmount"  : {
        #     "value"      : str(amount),
        #     "currency"   : "INR",
        #     },
        #     "userInfo": {
        #         "custId": str(email),
        #     },
        # }
        #
        # # Generate checksum by parameters we have in body
        # # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        # checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), Paytm_Key)
        #
        # paytmParams["head"] = {
        #     "signature": checksum
        # }
        #
        # post_data = json.dumps(paytmParams)
        #
        # # for Staging
        # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        #
        # # for Production
        # # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        # response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        # pay_page = {
        # "mid": Paytm_id,
        # "txnToken":response['body']['txnToken'],
        # "order_id": paytmParams['body']['order_id'],}

        # return render(request, 'shop/paytm.html', {'param_dict': pay_page})
    return render(request, 'shop/checkout.html')

# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'shop/paymentstatus.html', {'response': response_dict})