from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Capsule
from django.http import JsonResponse,HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import requests

DEBUG = False

# Create your views here.

@login_required
def index(request):
    return render(request,'shop/index.html')

@login_required
def shop(request):
    capsules_vertuo = Capsule.objects.filter(type_capsule='vertuo',stock__gt = 0)
    capsules_classique = Capsule.objects.filter(type_capsule='classique')

    context = {
        'capsules_vertuo': capsules_vertuo,
        'capsules_classique': capsules_classique
    }
    
    return render(request, 'shop/index.html', context)

@csrf_protect
def order_capsule(request):
    DEBUG = False

    if request.method == 'POST':
        
        vendor_token = '632b3978223b2045410032'
        url = "https://homologation.lydia-app.com/api/request/do.json"

        capsule_amount = request.POST.get('capsule_prix')  # Assuming you send the capsule_id in the POST request
        account_num = request.POST.get('account_num')

        # Modify the data dictionary with dynamic values based on the capsule_id or any other relevant information
        data = {
            "amount": int(capsule_amount)/100,
            "payment_method": "auto",
            "vendor_token": vendor_token,
            "recipient": account_num,
            "currency": "EUR",
            "type": "phone",
            
        }

        response = requests.post(url, data=data)
        if response.status_code == 200 : 
            
            transaction_data = response.json()
            redirect_url = transaction_data['mobile_url']
            
            if DEBUG : print(f"transaction data : {transaction_data}")

            return JsonResponse({'success': True, 'message': f'request to {url} SUCCEED', 'redirect' : redirect_url})
        else : 
            return JsonResponse({'success': False, 'message': f'request to {url} FAILED with status code {response.status_code}'})

    else:
        allowed_methods = ['POST']
        return HttpResponseNotAllowed(allowed_methods)