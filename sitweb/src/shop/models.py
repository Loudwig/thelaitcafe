from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return f'capsule_images/{instance.nom}/{filename}'

class Capsule(models.Model):
    TYPE_CAPSULE_CHOICES = [
        ('vertuo', 'Vertuo'),
        ('classique', 'Classique'),
    ]

    TYPE_CAFEINE_CHOICES = [
        ('cafeine', 'Caféiné'),
        ('decafeine', 'Décaféiné'),
    ]

    nom = models.CharField(max_length=255)
    prix_en_centimes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(50, message='Le prix doit être d\'au moins 50 centimes.'), MaxValueValidator(100, message='Le prix doit être d\'au plus 1 euro.')]
    )
    intensite = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    type_capsule = models.CharField(max_length=10, choices=TYPE_CAPSULE_CHOICES)
    type_cafeine = models.CharField(max_length=10, choices=TYPE_CAFEINE_CHOICES)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)  # Ajout du champ de stock


    def __str__(self):
        return self.nom

class Transaction(models.Model):
    request_id = models.CharField(max_length=30) # id de la transaction
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.ForeignKey(Capsule, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.request_id