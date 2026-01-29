from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment_review', 'rating_review')

        widgets = {
            'comment_review': forms.Textarea(attrs={
                'class': 'sidebar-text-search-box',
                'placeholder': 'Write your thoughts about the movie....',
                'rows': 4,
            }),
            'rating_review': forms.Select(attrs={
                'class': 'sidebar-text-search-box',
            }, choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }