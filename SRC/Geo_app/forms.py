from django import forms

from .models import Geo_distance


class DistanceForm(forms.ModelForm):
    class Meta:
        model = Geo_distance
        fields = ("destination",)