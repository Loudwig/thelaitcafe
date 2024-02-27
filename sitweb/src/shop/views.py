from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Capsule,Transaction
from django.http import JsonResponse,HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_protect
import requests
import json


from django.conf import settings
DEBUG = settings.DEBUG



@login_required
def shop(request):
    capsules_vertuo = Capsule.objects.filter(type_capsule='vertuo',stock__gt = 0)
    capsules_classique = Capsule.objects.filter(type_capsule='classique')
    user_phone_number = request.user.phone_number
    print(user_phone_number)
    context = {
        'capsules_vertuo': capsules_vertuo,
        'capsules_classique': capsules_classique,
        'phone_number' : user_phone_number
    }
    
    return render(request, 'shop/index.html', context)

@csrf_protect
def order_capsule(request):
    DEBUG = False

    if request.method == 'POST':
        
        vendor_token = '632b3978223b2045410032'
        url = "https://homologation.lydia-app.com/api/request/do.json"

        capsule_amount = request.POST.get('capsule_prix')  
        account_num = request.POST.get('account_num')
        capsule_name = request.POST.get('capsule_nom')

        data = {
            "amount": int(capsule_amount)/100, #vérifier ce truc
            "payment_method": "auto",
            "vendor_token": vendor_token,
            "recipient": account_num, # account_num à récupérer dans l'utilisateur
            "currency": "EUR",
            "type": "phone",
            
        }

        response = requests.post(url, data=data)
        if response.status_code == 200 : 
            transaction_data = response.json()
            
            # Créer une transation en cours 
            current_user = request.user
            capsule = Capsule.objects.get(nom=capsule_name)  # Remplacez 'nom_capsule' par le nom de la capsule réelle
            new_transaction = Transaction.objects.create(request_id = transaction_data["request_id"],author=current_user, contenu=capsule)
            
            redirect_url = transaction_data['mobile_url']
            
            if DEBUG : print(f"transaction data : {transaction_data}")

            return JsonResponse({'success': True, 'message': f'request to {url} SUCCEED', 'redirect' : redirect_url})
        else : 
            return JsonResponse({'success': False, 'message': f'request to {url} FAILED with status code {response.status_code}'})
            # what if that failes

    else:
        allowed_methods = ['POST']
        return HttpResponseNotAllowed(allowed_methods)



        