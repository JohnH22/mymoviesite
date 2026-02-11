from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

# Custom Form for Registration with Email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter your email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        # Using the fields from UserCreationForm (username, pass1, pass2) plus the email
        fields = UserCreationForm.Meta.fields + ('email',)

        # Check if the email is already used
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already in use.')
            return email
