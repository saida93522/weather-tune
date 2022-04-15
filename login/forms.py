from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"my_username",
                "id":"floatingInputUsername",
                }))
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class":"form-control",
                "placeholder":"Email",
                "id":"floatingInputEmail",
            }))
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                "placeholder":"Password",
                "id":"floatingPassword"}))

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "type":"text",
                "class":"form-control",
                "placeholder":"Confirm Password",
                "id":"floatingPasswordConfirm"            
        }))

    def clean_username(self):
        invalid_username = ['abc',123]
        username = self.cleaned_data['username']
        qs = User.objects.filter(username__iexact=username)
        
        if username in invalid_username:
            raise forms.ValidationError("This is an invalid username, please choose a different username.")        
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please choose a different username.")
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"my_username",
                "id":"floatingInput"}))

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                "placeholder":"Password",
                "id":"floatingPassword"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError('Invalid username, please enter valid username.')
        return username