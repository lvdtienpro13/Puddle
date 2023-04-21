from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'You username',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'You password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'password1','password2')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'You username',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'You email',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'You password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))

class SettingProfileForm(forms.ModelForm):
    firstname = forms.CharField(max_length=30, required=True)
    lastname = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Profile
        fields = ('profileimg','firstname', 'lastname','bio','location')
        widgets = {
            'profileimg': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'firstname': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'lastname': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'bio': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'location': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            
            
        }
    def save(self, commit=True):
        profile = super(SettingProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        if commit:
            profile.save()
            user.save()
        return profile
    
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Old password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'You password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'peer block min-h-[auto] w-full rounded border-0 bg-transparent py-[0.32rem] px-3 leading-[2.15] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:text-neutral-200 dark:placeholder:text-neutral-200 [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0'
    }))