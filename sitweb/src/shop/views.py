from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Capsule
# Create your views here.

@login_required
def index(request):
    return render(request,'shop/index.html')

@login_required
def shop(request):
    type_capsule = request.GET.get('type_capsule', 'vertuo')  # par défaut, affiche les produits Vertuo
    capsules = Capsule.objects.filter(type_capsule=type_capsule)
    print(capsules)

    context = {
        'capsules': capsules,
        'type_capsule': type_capsule,
    }
    for capsule in Capsule.objects.all():
        print(capsule.image.url)
    return render(request, 'shop/index.html', context)
