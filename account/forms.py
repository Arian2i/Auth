from django import forms
from . models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin"]


def start_with_0(value):  # شماره باید با صفر شروع شود
    if value[0] != '0':
        raise forms.ValidationError("Phone Should Start With '0' ")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):  # بخش خاصی اعتبار سنجی
        username = self.cleaned_data.get('username')
        if len(username) > 50 or len(username) < 2:
            raise ValidationError(
                "Invalid value: %(value)s is invalid, Phone must have 11 char",
                code="invalid",
                params={"value": f'{username}'},
            )

        return username

    '''def clean(self):  # برای بخش خاصی نباشه اعتبار سنجی
        cd = super().clean()
        phone = cd['phone']
            
        phone = self.cleaned_data.get('phone')
        if len(phone) > 11 or len(phone) < 10:
            raise ValidationError(
                "Invalid value: %(value)s is invalid, Phone must have 11 char",
                code="invalid",
                params={"value": f'{phone}'},
        )
            
        return phone'''


class OtpLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(50)])


class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(4)])
