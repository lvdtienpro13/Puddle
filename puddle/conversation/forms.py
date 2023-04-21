from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields= ('content',)
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'w-full text-lg py-2 px-4 rounded-xl border'
            })
        }
