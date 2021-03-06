# core django imports
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserNameForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
