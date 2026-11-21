from django import forms
import re

class RecipeForm(forms.Form):
    title = forms.CharField(max_length=100, label='Название рецепта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(max_length=100, label='Автор', widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(max_length=50, label='Категория', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cooking_time = forms.IntegerField(min_value=1, max_value=1440, label='Время готовки (мин)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ingredients = forms.CharField(label='Ингредиенты (через запятую)', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    description = forms.CharField(required=False, label='Описание', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    file_format = forms.ChoiceField(choices=[('json', 'JSON'), ('xml', 'XML')], label='Формат файла', widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    save_to = forms.ChoiceField(choices=[('file', 'В файл'), ('db', 'В базу данных')], label='Куда сохранить', widget=forms.Select(attrs={'class': 'form-select'}))

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if not re.match(r'^[\w\s\-.,()]+$', title, re.UNICODE):
            raise forms.ValidationError('Недопустимые символы.')
        return title

    def clean_ingredients(self):
        items = [i.strip() for i in self.cleaned_data['ingredients'].split(',') if i.strip()]
        if not items:
            raise forms.ValidationError('Укажите ингредиенты.')
        return items