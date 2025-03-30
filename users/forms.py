from django import forms
from django.contrib.auth.models import User
from . models import Profile

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username','email','password','confirm_password')

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if len(password) > 7:
            if password and confirm_password:
                if password != confirm_password:
                    raise forms.ValidationError(
                        "Password and Confirm Password didn't match"
                    )
        else:
            raise forms.ValidationError(
                "Password must have atleast 8 characters"
            )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'gender',
            'birth_day',
            'about',
            'school',
            'work',
            'skills',
            'current_city',
#            'phon_no',
            'website',
            'image'
            ]

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(required = True)

class PasswordResetForm(forms.Form):
    username = forms.CharField(required = True)

class OtpVerificationForm(forms.Form):
    otp = forms.CharField(required = True)
