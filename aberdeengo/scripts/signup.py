from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("username"), error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("password1"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("password2"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='upload profile picture',
    )


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        # If the user entered the current password, make sure it's right
        if self.cleaned_data['current_password'] and not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError('This is not your current password. Please try again.')

        # If the user entered the current password, make sure they entered the new passwords as well
        if self.cleaned_data['current_password'] and not (self.cleaned_data['password'] or self.cleaned_data['confirm_password']):
            raise forms.ValidationError('Please enter a new password and a confirmation to update.')

        return self.cleaned_data['current_password']

    def clean_confirm_password(self):
        # Make sure the new password and confirmation match
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Your passwords didn't match. Please try again.")

        return self.cleaned_data.get('confirm_password')
