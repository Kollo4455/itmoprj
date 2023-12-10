from django import forms
from .models import Pickle_model


class ModelForm(forms.ModelForm):
    class Meta:
        model = Pickle_model
        fields = ['name']  # Поля, которые будут отображаться в форме

    # Дополнительные поля для формы (не из модели)
    excel_file = forms.FileField(label='Upload Excel File')
    model_choice = forms.ModelChoiceField(queryset=Pickle_model.objects.all(), label='Choose Model')

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['model_choice'].queryset = Pickle_model.objects.filter(user=user)

    def save(self, user, commit=True):
        instance = super(ModelForm, self).save(commit=False)
        instance.user = user
        # Обработка загруженного Excel файла
        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            # Обработка файла (ваш код)
            pass
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ModelSelectionForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File')
    user_models = forms.ModelChoiceField(queryset=None, label='Your Models')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ModelSelectionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user_models'].queryset = Pickle_model.objects.filter(user=user)
