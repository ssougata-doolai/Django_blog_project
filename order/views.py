import razorpay
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
client = razorpay.Client(auth=("rzp_test_Qrum48VNd3R8T4", "J3cS08M6EoJRBF1M1o5uVWGu"))

def create_order(request):
    order_amount = 5000
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    resp = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
    id = resp['id']
    return render(request, 'order/create.html', {'id': id})
    #return redirect('https://rzp.io/l/Fp59h7G')


@csrf_exempt
def checkout(request):
    params_dict = {
        'razorpay_order_id': request.POST.get('razorpay_order_id'),
        'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
        'razorpay_signature': request.POST.get('razorpay_signature')
    }
    # client.utility.verify_payment_signature(params_dict)
    try:
        client.utility.verify_payment_signature(params_dict)
        messages.success(request,"Payment successful")
    except:
        messages.success(request,"Payment failed")
    return HttpResponseRedirect(reverse('blogs:blogs-index'))
