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

    if request.method == 'POST':
        
        vendor_token = '632b3978223b2045410032'
        url = "https://homologation.lydia-app.com/api/request/do.json"

        capsule_amount = request.POST.get('capsule_prix')  
        account_num = request.POST.get('phone_number')
        capsule_name = request.POST.get('capsule_nom')
        print(f'account num : {account_num}')
        message = f"ACHAT DE LA CAPSULE : {capsule_name}"
        
        data = {
            "amount": int(capsule_amount)/100, #vérifier ce truc
            "payment_method": "auto",
            "vendor_token": vendor_token,
            "recipient": str(account_num), # account_num à récupérer dans l'utilisateur
            "currency": "EUR",
            "type": "phone",
            "message" : message,
        }

        response = requests.post(url, data=data)
        if response.status_code == 200 : 
            transaction_data = response.json()
            
            if DEBUG : print(f"transaction data : {transaction_data}")
            
            if transaction_data['error'] == '0' : 
                # Créer une transation en cours 
                current_user = request.user
                capsule = Capsule.objects.get(nom=capsule_name)  # Remplacez 'nom_capsule' par le nom de la capsule réelle
                new_transaction = Transaction.objects.create(request_id = transaction_data["request_id"],author=current_user, contenu=capsule)
                
                redirect_url = transaction_data['mobile_url']
                
                return JsonResponse({'success': True, 'message': f'request to {url} SUCCEED', 'redirect' : redirect_url})
            else : 
                return JsonResponse({'success': False, 'message': f'transaction failed with error {transaction_data["error"]} | message : {transaction_data["message"]}'})
        else : 
            return JsonResponse({'success': False, 'message': f'request to {url} FAILED with status code {response.status_code}'})

    else:
        allowed_methods = ['POST']
        return HttpResponseNotAllowed(allowed_methods)



        