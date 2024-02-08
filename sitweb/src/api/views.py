from django.shortcuts import render
from shop.models import Capsule,Transaction
from django.http import JsonResponse,HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login

from django.conf import settings
DEBUG = settings.DEBUG

# The arduino request this view to get the transaction that havec been paid
def est_superuser(user):
    print(user.is_superuser)
    print("")
    if user.is_superuser :
        print( "user is  superuser") 
        print(user)
        return user.is_superuser
    else : 
        print( "user is not superuser")
        print(user)
        return user.is_superuser

@csrf_exempt
def api_login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Authentication failure'}, status=401)


    return HttpResponse('Method Not Allowed', status=405)

@user_passes_test(est_superuser)
@csrf_exempt
def getTransaction(request):
    if request.method == 'POST': 
        transac = Transaction.objects.filter(status=1)
        transac_list = [ transaction.data() for transaction in transac]
        return JsonResponse({'transactions': transac_list})
    
    else : 
        if DEBUG : 
            transac = Transaction.objects.filter(status=1)
            transac_list = [ transaction.data() for transaction in transac]
            context = {'transactions': transac_list}
            return render(request,'api/getTransaction.html',context)
        else : 
            allowed_methods = ['POST']
            return HttpResponseNotAllowed(allowed_methods)



# When a transaction as been treated by the arduino they recieve code 300
# It prevents that the arduino retreat them

@user_passes_test(est_superuser)
@csrf_exempt
def update(request):

    if request.method == 'POST' : 
        data = json.loads(request.body.decode('utf-8'))
        response = data.get("request_id")

        transToUpdate = Transaction.objects.filter(request_id = response)
        
        for trans in transToUpdate:
            trans.status = 300 
            trans.save()
            if  DEBUG : print(f'transaction {trans.request_id} is updated')
        
        return JsonResponse({'success': True})
