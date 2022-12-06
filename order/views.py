from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import OrderForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from store.models import *
from django.contrib import messages
import requests
import json
from core.settings import MERCHANT
from shipping.models import WeightPrice


@login_required
def order_form(request):
    cart = Cart(request)
    if not cart:
        return redirect('/')
    form = OrderForm()
    provinces = Provinces.objects.all()
    return render(request, 'order/order_form.html', {'form': form, 'provinces': provinces})


def order_create(request):
    form = OrderForm(request.POST or None)
    if request.user.is_authenticated and request.user.is_verify:
        if request.method == 'POST':
            cart = Cart(request)
            if cart:
                if form.is_valid():
                    data = form.cleaned_data
                    order = Order.objects.create(
                        user_id=request.user.id,
                        province=data['province'],
                        city=data['city'],
                        address=data['address'], phone=data['phone'], first_name=data['first_name'],
                        last_name=data['last_name'], order_description=data['order_description'],
                        status='not_paid',
                        order_code=get_random_string(length=10)
                    )
                    obj_weight = 0
                    for data in cart:
                        obj_weight += int(data['variant'].product.weight * data['quantity'])

                    # total_weight_price(order, total_weight)
                    weight_price = WeightPrice.objects.last()
                    if obj_weight <= 500:
                        order.shipping_price = int(weight_price.price_0_to_half)
                        order.save()
                    elif obj_weight > 500 and obj_weight <= 1000:
                        order.shipping_price = int(weight_price.price_half_to_1)
                        order.save()
                    elif obj_weight > 1000 and obj_weight <= 2000:
                        order.shipping_price = int(weight_price.price_1_to_2)
                        order.save()
                    elif obj_weight > 2000 and obj_weight <= 3000:
                        order.shipping_price = int(weight_price.price_2_to_3)
                        order.save()
                    elif obj_weight > 3000 and obj_weight <= 4000:
                        order.shipping_price = int(weight_price.price_3_to_4)
                        order.save()
                    elif obj_weight > 4000 and obj_weight <= 5000:
                        order.shipping_price = int(weight_price.price_4_to_5)
                        order.save()
                    elif obj_weight > 5000 and obj_weight <= 6000:
                        order.shipping_price = int(weight_price.price_5_to_6)
                        order.save()
                    elif obj_weight > 6000 and obj_weight <= 7000:
                        order.shipping_price = int(weight_price.price_6_to_7)
                        order.save()
                    elif obj_weight > 7000 and obj_weight <= 8000:
                        order.shipping_price = int(weight_price.price_7_to_8)
                        order.save()
                    elif obj_weight > 8000 and obj_weight <= 9000:
                        order.shipping_price = int(weight_price.price_8_to_9)
                        order.save()
                    elif obj_weight > 9000 and obj_weight <= 10000:
                        order.shipping_price = int(weight_price.price_9_to_10)
                        order.save()
                    elif obj_weight > 10000 and obj_weight <= 11000:
                        order.shipping_price = int(weight_price.price_10_to_11)
                        order.save()
                    elif obj_weight > 11000 and obj_weight <= 12000:
                        order.shipping_price = int(weight_price.price_11_to_12)
                        order.save()
                    elif obj_weight > 12000 and obj_weight <= 13000:
                        order.shipping_price = int(weight_price.price_12_to_13)
                        order.save()
                    elif obj_weight > 13000 and obj_weight <= 14000:
                        order.shipping_price = int(weight_price.price_13_to_14)
                        order.save()
                    elif obj_weight > 14000 and obj_weight <= 15000:
                        order.shipping_price = int(weight_price.price_14_to_15)
                        order.save()
                    elif obj_weight > 15000 and obj_weight <= 16000:
                        order.shipping_price = int(weight_price.price_15_to_16)
                        order.save()
                    elif obj_weight > 16000 and obj_weight <= 17000:
                        order.shipping_price = int(weight_price.price_16_to_17)
                        order.save()
                    elif obj_weight > 17000 and obj_weight <= 18000:
                        order.shipping_price = int(weight_price.price_17_to_18)
                        order.save()
                    elif obj_weight > 18000 and obj_weight <= 19000:
                        order.shipping_price = int(weight_price.price_18_to_19)
                        order.save()
                    elif obj_weight > 19000 and obj_weight <= 20000:
                        order.shipping_price = int(weight_price.price_19_to_20)
                        order.save()
                    elif obj_weight > 20000 and obj_weight <= 21000:
                        order.shipping_price = int(weight_price.price_20_to_21)
                        order.save()
                    elif obj_weight > 21000 and obj_weight <= 22000:
                        order.shipping_price = int(weight_price.price_21_to_22)
                        order.save()
                    elif obj_weight > 22000 and obj_weight <= 23000:
                        order.shipping_price = int(weight_price.price_22_to_23)
                        order.save()
                    elif obj_weight > 23000 and obj_weight <= 24000:
                        order.shipping_price = int(weight_price.price_23_to_24)
                        order.save()
                    elif obj_weight > 24000 and obj_weight <= 25000:
                        order.shipping_price = int(weight_price.price_24_to_25)
                        order.save()
                    elif obj_weight > 25000 and obj_weight <= 26000:
                        order.shipping_price = int(weight_price.price_25_to_26)
                        order.save()
                    elif obj_weight > 26000 and obj_weight <= 27000:
                        order.shipping_price = int(weight_price.price_26_to_27)
                        order.save()
                    elif obj_weight > 27000 and obj_weight <= 28000:
                        order.shipping_price = int(weight_price.price_27_to_28)
                        order.save()
                    elif obj_weight > 28000 and obj_weight <= 29000:
                        order.shipping_price = int(weight_price.price_28_to_29)
                        order.save()
                    elif obj_weight > 29000 and obj_weight <= 30000:
                        order.shipping_price = int(weight_price.price_29_to_30)
                        order.save()
                    elif obj_weight > 30000:
                        order.shipping_price = int(weight_price.price_30_to_higher)
                        order.save()

                    for item in cart:
                        ItemOrder.objects.create(
                            user_id=request.user.id,
                            order_id=order.id,
                            variant=item['variant'],
                            price=item['variant'].total_price,
                            console_guarantee=item['variant'].console_variant,
                            controller_guarantee=item['variant'].controller_variant,
                            unit_price=item['variant'].unit_price,
                            discount=item['variant'].discount_variant,
                            quantity=item['quantity']
                        )
                    cart.clear()
                    return redirect('order:order_complete', order.id)
            else:
                messages.warning(request, 'سبد خرید شما خالی است!')
                return redirect('/')
        else:
            return redirect('store:home_page')
    else:
        return redirect('/')


@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # check if order is for this user and is not paid then show the payment page
    if request.user.id == order.user_id and not order.is_paid:
        return render(request, 'order/order_complete.html', {'order': order})
    # check if order is for this user and if it`s paid then redirect user
    elif request.user.id == order.user.id and order.is_paid:
        messages.info(request, f'سفارش {order.order_code} برای شما پرداخت شده است.')
        return redirect('accounts:order_list')
    else:
        return redirect('store:home_page')


def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = Cities.objects.filter(province_id=province_id)
    return render(request, 'order/cities_list_options.html', {'cities': cities})


@login_required
def order_is_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.id == order.user_id:
        items = order.item_orders.all()
        return render(request, 'order/order_is_paid.html', {'order': order, 'items': items})
    else:
        return redirect('store:home')


MERCHANT = MERCHANT
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 10000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify/'


@login_required
def send_request_payment(request, pk, price):
    global userOrderId, amount
    userOrderId = pk
    amount = price
    order = Order.objects.get(user_id=request.user.id, id=userOrderId, is_paid=False)
    # Update Order Price Before Payment If Prices Changes
    for item in order.item_orders.all():
        item.price = item.variant.total_price
        item.unit_price = item.variant.unit_price
        item.discount = item.variant.discount_variant
        item.save()
        order.save()
    order.save()
    # End Update Order Price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order = Order.objects.get(id=userOrderId, user_id=request.user.id)
                order.is_paid = True
                order.status = 'P'
                order.save()
                items = ItemOrder.objects.filter(order_id=userOrderId, user_id=request.user.id)
                for data in items:
                    product = Product.objects.get(id=data.variant.product.id)
                    product.sell += data.quantity
                    product.save()
                    variant = Variants.objects.get(id=data.variant.id)
                    variant.v_amount -= data.quantity
                    variant.save()
                return redirect('accounts:order_list')
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
