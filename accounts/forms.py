from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import User


# this form is for adding user in admin panel
class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, label='تکرار رمز عبور')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('check password please')
        return data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email']

    def clean_password(self):
        return self.initial['password']


class RegisterForm(forms.Form):
    first_name_form = forms.CharField(
        label='نام',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }
        ),
    )
    last_name_form = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }
        ),
    )
    email_form = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    phone_number_form = forms.CharField(
        label='شماره همراه',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '*********09'
            }
        ),
        validators=[
            validators.MaxLengthValidator(11),
        ]
    )
    password_form = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور'
            }
        ),
        validators=[
            validators.MinLengthValidator(8)
        ]

    )
    confirm_password_form = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'تکرار رمز عبور'
            }
        ),
        validators=[
            validators.MinLengthValidator(8)
        ]
    )

    # check if username exists in database
    # def clean_user_name_form(self):
    #     user_name = self.cleaned_data['user_name_form']
    #     if User.objects.filter(username=user_name).exists():
    #         raise forms.ValidationError('این نام کاربری از قبل موجود است')
    #     return user_name

    def clean_email_form(self):
        email = self.cleaned_data['email_form']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('این ایمیل از قبل موجود است')
        return email

    def clean_confirm_password_form(self):
        password = self.cleaned_data['password_form']
        confirm_password = self.cleaned_data['confirm_password_form']

        if password != confirm_password:
            raise forms.ValidationError('کلمات عبور با هم مغایرت دارند. لطفا دوباره تلاش کنید.')
        # elif len(confirm_password) < 10:
        #     raise forms.ValidationError('رمز عبور نباید کمتر از 10 کاراکتر باشد.')
        # elif not any(p.isupper() for p in confirm_password):
        #     raise forms.ValidationError('باید از حداقل یک حرف بزرگ استفاده کنید.')
        # elif not any(p.islower() for p in confirm_password):
        #     raise forms.ValidationError('باید از حداقل یک حرف کوچک استفاده کنید.')
        return confirm_password


class LoginForm(forms.Form):
    phone_number_form = forms.CharField(
        label='شماره همراه',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'شماره همراه'
            }
        ),
        # validators=[
        #     validators.MaxLengthValidator(100),
        # ]
    )
    password_form = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور'
            }
        ),
    )

    def clean(self):
        if self.is_valid():
            phone = self.cleaned_data['phone_number_form']
            password = self.cleaned_data['password_form']
            if not authenticate(phone=phone, password=password):
                raise forms.ValidationError("شماره یا رمز عبور اشتباه است.")


class ResetPasswordEmailValidation(PasswordResetForm):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'لطفا ایمیل خود را وارد نمایید.'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("کاربری با مشخصات وارد شده وجود ندارد.")
        return email


class VerifyRegistrationForm(forms.Form):
    code = forms.IntegerField(
        label='کد تایید',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'کد تایید'
            }
        ))

    # def clean(self):
    #     code = self.cleaned_data['code']
    #     if User.objects.filter(is_verify=True).exists():
    #         raise ValidationError("شما کاربر فعال میباشید.")
    #     return code


class ForgotPasswordForm(forms.Form):
    phone_number_form = forms.CharField(
        label='شماره همراه',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'شماره همراه'
            }
        ),
    )

    def clean_phone_number_form(self):
        phone_number = self.cleaned_data['phone_number_form']
        if not User.objects.filter(phone__iexact=phone_number, is_active=True).exists():
            raise forms.ValidationError("کاربری با مشخصات وارد شده وجود ندارد.")
        return phone_number


class VerifyResetPassword(forms.Form):
    reset_password_code = forms.IntegerField(
        label='کد تایید',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'کد تایید'
            }
        ))
    reset_password_form = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور جدید'
            }
        ),
        validators=[
            validators.MinLengthValidator(8)
        ]

    )
    confirm_reset_password_form = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'تکرار رمز عبور جدید'
            }
        ),
        validators=[
            validators.MinLengthValidator(8)
        ]
    )

    def clean_confirm_reset_password_form(self):
        reset_password = self.cleaned_data['reset_password_form']
        confirm_reset_password = self.cleaned_data['confirm_reset_password_form']

        if reset_password != confirm_reset_password:
            raise forms.ValidationError('کلمات عبور با هم مغایرت دارند. لطفا دوباره تلاش کنید.')
        return confirm_reset_password


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['phone'].disabled = True

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'province', 'city', 'post_code', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'post_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور فعلی'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور جدید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    confirm_new_password = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'تایید رمز عبور'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_new_password(self):
        password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_new_password']

        if password != confirm_password:
            raise forms.ValidationError('کلمات عبور با هم مغایرت دارند. لطفا دوباره تلاش کنید.')
        return confirm_password
