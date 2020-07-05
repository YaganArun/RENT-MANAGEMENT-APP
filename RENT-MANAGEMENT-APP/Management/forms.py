from django import forms
from .models import Person
from .models import Person
class PersonForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30 , required=False)
    age = forms.IntegerField(required=False)
    designation = forms.CharField(max_length=20 , required=False)
    room_no = forms.CharField(max_length=10)
    rent_Ammount = forms.IntegerField()
    advance_Ammount = forms.IntegerField()
    contact_no = forms.IntegerField(required=False)
    date = forms.DateField(widget=forms.SelectDateWidget())

class RentForm(forms.Form):
    rent = forms.IntegerField()
    electric_bill = forms.IntegerField()
    Maintanace_charge = forms.IntegerField(required=False)
    # paymentDate = forms.DateField(widget=forms.SelectDateWidget(), disabled=True)

class RentFormOld(forms.Form):
    rent = forms.IntegerField()
    electric_bill = forms.IntegerField()
    Maintanace_charge = forms.IntegerField(required=False)
    paymentDate = forms.DateField(widget=forms.SelectDateWidget())

