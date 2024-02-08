import os
import django
import requests
from time import sleep

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boutique.settings")

django.setup()

# vérifier le stock juste avant de payer

from shop.models import Transaction  

vendortoken = '632b3978223b2045410032'
url = "https://homologation.lydia-app.com//api/request/state.json"
cancel_url = "https://homologation.lydia-app.com//api/request/cancel.json"
DEBUG = True
TIME_DELAY = 5


def stateTransaction(id):
    # data pour la requête
    data = {
    "request_id": id,
    "vendor_token": vendortoken
    }
    response = requests.post(url, data=data)

    if response.status_code == 200 : 
        payment_data = response.json()
        if DEBUG : print(f"payment data of transaction {id} : {payment_data}")
        if int(payment_data['state']) == 0 :
            return 0
        if int(payment_data['state']) == 1:
            return 1
        if int(payment_data['state']) == 5 :
            return 5
        if int(payment_data['state']) == 6:
            return 6
        if int(payment_data['state'])==-1:
            return -1
        

    else : 
        print(f"requete failed with status code {response.status_code}")
        return 0

def stockUp(t):
    
    if t.contenu.stock > 0 : 
        return True
    
    else : 
        return False


while True : 
    transactionWaiting = Transaction.objects.filter(status=0).all()
    
    for ind,transaction in enumerate(transactionWaiting):
        
        

        if stockUp(transaction):
            
            
            if DEBUG:
                print(transaction)
                print(f"stock is up for transaction {transaction.request_id}")

            if stateTransaction(transaction.request_id) == 1 : 
                print(f"La transaction {transaction.request_id} a été PAYÉ")
                transaction.status = 1 # passe le statut de la transaction en transaction payé
                
                transaction.contenu.stock = transaction.contenu.stock -1 # uptdate stock
                transaction.contenu.save() # uptdate stock
                transaction.save()
                

            elif stateTransaction(transaction.request_id) == 0 : 
                print(f'La transaction {transaction.request_id} est EN COURS')

            elif stateTransaction(transaction.request_id) == 5 : 
                print(f"La transaction {transaction.request_id} a été refusé par l'utilisateur")
                transaction.status = 5
                transaction.save()

            elif stateTransaction(transaction.request_id) == 6 : 
                print(f'La transaction {transaction.request_id} a été cancelled')
                transaction.status = 6
                transaction.save()
            
            elif stateTransaction(transaction.request_id) == -1 : 
                print(f'La transaction {transaction.request_id} a un status inconnu')
        
        else :  
            data = {
                "request_id" : transaction.request_id,
                "vendor_token": vendortoken
            }
            cancel = requests.post(url = cancel_url, data = data)
            print(f'La transaction {transaction.request_id} a été cancelled')
            transaction.status = 6
            transaction.save()
            print(cancel.json())

    sleep(TIME_DELAY)
    

