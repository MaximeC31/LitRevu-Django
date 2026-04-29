from django.db import models


class Person(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    age = models.IntegerField()
    numero = models.CharField(max_length=20)
    voie = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def presentation(self):
        return f"{self.prenom} {self.nom}, {self.age} ans"

    def adresse_complete(self):
        return f"{self.numero} {self.voie}, {self.code_postal} {self.ville}"
