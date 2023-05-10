from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'rating_comment')
        widgets = {
            'rating_comment': forms.Textarea(attrs={'rows': 4})
        }