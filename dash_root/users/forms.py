from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nickname",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your nickname",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "autocomplete": "current-password",
        })
    )