from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text","group",)
        group = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            required=False,
            to_field_name="id_group",
        )
        widgets = {
            'text': forms.Textarea(),
        }

        labels = {
            "group": "Группа",
            "text": "Текст",
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == '':
            raise forms.ValidationError(
                'Заполните, пожалуйста, обязательное поле!'
            )
        return text
