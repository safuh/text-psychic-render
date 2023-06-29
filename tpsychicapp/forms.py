from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100)
	password = forms.CharField(widget = forms.PasswordInput())

class CreateForm(forms.Form):
	username = forms.CharField(max_length = 100)
	password = forms.CharField(widget = forms.PasswordInput())

class DocForm(forms.Form):
	##myfile = forms.FileField()##TODO
	message = forms.CharField()