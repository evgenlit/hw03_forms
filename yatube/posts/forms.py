from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == '':
            raise forms.ValidationError(
                'Заполните, пожалуйста, обязательное поле!'
            )
        return text