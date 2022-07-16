from django.db import models


class Geo_distance(models.Model):
    location= models.CharField(max_length=200)
    destination=models.CharField(max_length=200)
    distance=models.DecimalField(max_digits=10, decimal_places=2)
    Created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"La distance de {self.location} à {self.destination} est de {self.distance} km"
