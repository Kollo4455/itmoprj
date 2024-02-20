import os

import joblib
import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from .forms import ModelForm, ModelSelectionForm
from django.contrib import messages

# Create your views here.
from .models import PickleModel


@login_required
def upload_model(request):
    if request.method == 'POST':
        form = ModelForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            form.save(request.user, name)
            messages.success(request, f'Модель успешно обучена')

            # Обработка после успешной загрузки

    else:
        form = ModelForm(request.user)
    return render(request, 'itmo/upload_model.html',
                  {
                      'form': form,
                      'title': 'Обучение модели',
                  })


def error_404_view(request):
    return render(request, '404.html', {})


def process_form(pickle_path, form):
    # Обработка формы при отправке
    excel_file = form.cleaned_data['excel_file']
    user_models = form.cleaned_data['user_models']

    # Получение пути до пикл файла выбранной модели, если модель выбрана
    if user_models:
        pickle_path = user_models.pickle.path if user_models.pickle else None

    automl = joblib.load(pickle_path)
    data = pd.read_csv(excel_file)
    return automl.predict(data).data[:, 0]


@login_required
def model_selection_view(request):
    pickle_path = None  # Инициализация переменной pickle_path

    if request.method == 'POST':
        form = ModelSelectionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            pred = process_form(pickle_path, form)
            return render(request, 'itmo/results_page.html',
                          {'pickle_path': pickle_path,
                           'pred': pred})  # Передача pickle_path в шаблон результатов
    else:
        form = ModelSelectionForm(user=request.user)

    return render(request, 'itmo/model_selection.html',
                  {
                      'form': form,
                      'title': 'Предсказание',
                  })


def guid_view(request):
    return render(request, 'itmo/guid_page.html')


def download_template(request):
    # Путь к вашему файлу template.xlsx
    file_path = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="template.xlsx"'
            return response
    else:
        return HttpResponse("File not found", status=404)
