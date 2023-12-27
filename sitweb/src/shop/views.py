from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Capsule

DEBUG = True

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

