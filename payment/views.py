from django.shortcuts import render
from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse,get_object_or_404
from orders.models import Order
# Create your views here.
#create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id',None)
    order = get_object_or_404(Order,id=order_id)
    if request.method =='POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:cenceled'))
        session_data = {
            'mode':'payment',
            'client_reference_id':order.id,
            'success_url':success_url,
            'cancel_url':cancel_url,
            'line_items':[]
        }
        #create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        #redirect to stripe payment form
        return redirect(success_url,code=303)
    else:
        return render(request,'payment/process.html',locals())