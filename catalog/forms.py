import os
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Product




class ProductForm(forms.ModelForm):
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'photo', 'category', 'price']

    def _check_forbidden_words(self, text):
        lower_text = text.lower()
        for word in self.forbidden_words:
            if word in lower_text:
                return word
        return None

    def clean_name(self):
        name = self.cleaned_data['name']
        if forbidden_word := self._check_forbidden_words(name):
            raise forms.ValidationError(f'Содержит запрещенное слово: "{forbidden_word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if forbidden_word := self._check_forbidden_words(description):
            raise forms.ValidationError(f'Содержит запрещенное слово: "{forbidden_word}"')
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Проверка расширения файла
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = os.path.splitext(photo.name)[1].lower()  # Теперь os доступен
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    f"Неподдерживаемый формат. Разрешенные форматы: {', '.join(valid_extensions)}"
                )

            # Проверка содержимого файла
            try:
                from PIL import Image
                with Image.open(photo) as img:
                    img.verify()
            except Exception as e:
                raise ValidationError(f"Файл поврежден или не является изображением: {str(e)}")

            # Проверка размера файла (макс. 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError("Максимальный размер файла - 5 МБ")
        return photo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Общие стили для всех полей
        for field_name, field in self.fields.items():
            # Добавляем класс form-control для стандартных полей
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs['class'] = 'form-control'

            # Добавляем placeholder
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Опишите характеристики товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Цена в рублях'

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

        # Специальные настройки для отдельных полей
        self.fields['description'].widget.attrs.update({
            'rows': 4,
            'class': 'form-control description-field',
            'style': 'resize: vertical; min-height: 100px;'
        })

        self.fields['photo'].widget.attrs.update({
            'class': 'form-control visually-hidden',  # Скрываем стандартный input
            'accept': 'image/*',
            'onchange': 'previewImage(this)'
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })

        # Для чекбоксов (если они появятся в будущем)
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs['class'] = 'form-check-input'

        # Кастомные классы для ошибок
        self.error_css_class = 'is-invalid'
        self.required_css_class = 'required'