from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Capsule,Transaction
from django.http import JsonResponse,HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import requests
import json

DEBUG = False
API_KEY = '12'

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

    else:
        allowed_methods = ['POST']
        return HttpResponseNotAllowed(allowed_methods)



# The arduino request this view to get the transaction that havec been paid
@csrf_exempt
def getTransaction(request):
    api_key = request.headers.get('Authorization', '').split('Bearer ')[-1]
    
    if api_key != API_KEY:
        return JsonResponse({'error': 'Clé d\'authentification invalide'}, status=401)

    if request.method == 'POST': 
        transac = Transaction.objects.filter(status=1)
        transac_list = [ transaction.data() for transaction in transac]
        return JsonResponse({'transactions': transac_list})
    
    else : 
        if DEBUG : 
            transac = Transaction.objects.filter(status=1)
            transac_list = [ transaction.data() for transaction in transac]
            context = {'transactions': transac_list}
            return render(request,'shop/getTransaction.html',context)
        else : 
            allowed_methods = ['POST']
            return HttpResponseNotAllowed(allowed_methods)



# When a transaction as been treated by the arduino they recieve code 300
# It prevents that the arduino retreat them
@csrf_exempt
def update(request):
    
    # -----------SECURITY----------
    api_key = request.headers.get('Authorization', '').split('Bearer ')[-1]
    
    if api_key != API_KEY:
        return JsonResponse({'error': 'Clé d\'authentification invalide'}, status=401)
    # ----------SECURITY------------

    if request.method == 'POST' : 
        data = json.loads(request.body.decode('utf-8'))
        response = data.get("request_id")

        transToUpdate = Transaction.objects.filter(request_id = response)
        
        for trans in transToUpdate:
            trans.status = 300 
            trans.save()
            if  DEBUG : print(f'transaction {trans.request_id} is updated')
        
        return JsonResponse({'success': True})

        