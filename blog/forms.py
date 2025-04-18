from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Form for blog post comments"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (real or superhero identity)',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email (I promise not to spam you)',
                'class': 'form-control'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'Your website (totally optional)',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts, questions, or existential photography crisis',
                'rows': 5,
                'class': 'form-control'
            }),
        }
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError("Comment too short! At least add a few more words to make it interesting.")
        return content