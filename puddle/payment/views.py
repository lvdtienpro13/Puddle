from django.shortcuts import render, redirect
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from item.models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from core.models import Profile
from .forms import ShippingAddressForm
from .models import ShippingAddress
# Create your views here.

@csrf_exempt
def payment_done(request):
    pk = request.GET.get('pk')
    print(pk)
    order = get_object_or_404(Order, pk=pk)
    order.complete_order()
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled (request):
    return render(request, 'payment/canceled.html')

def payment_process(request, pk):
    order = get_object_or_404(Order, pk=pk)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(str(order.get_total())),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}?pk={}'.format(host, reverse('payment:done'), pk),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
        }
    # order.complete_order()
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order,
        'form': form,
        'pk':pk})


def checkout(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_total_price = order.get_total()
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    item_count = order_items.count()
    if request.method == 'POST':
    # Lấy dữ liệu từ form
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        # Tạo một đối tượng ShippingAddress từ dữ liệu trong form.
        shipping_address = ShippingAddress(name=name, address=address, email=email, phone_number=phone_number, user=request.user)
        # Lưu thông tin vận chuyển địa chỉ vào session.
        request.session['shipping_address'] = {
            'name': shipping_address.name,
            'address': shipping_address.address,
            'email': shipping_address.email,
            'phone_number': shipping_address.phone_number
        }
        shipping_address.save()
        order.shipping_address = shipping_address
        order.save()
        # Lưu session để giữ các thông tin địa chỉ vận chuyển cho các yêu cầu tiếp theo.
        request.session.modified = True
        
        return redirect('payment:process', pk=pk)  # Chuyển hướng đến trang thanh toán.

    else:
        # Lấy thông tin vận chuyển địa chỉ từ session nếu có.
        shipping_address_data = request.session.get('shipping_address', {})

    context ={
        'shipping_address_data': shipping_address_data,
        'order_items': order_items,
        'order_total_price':order_total_price,
        'item_count': item_count,
    }

    return render(request, 'payment/checkout.html', context)
