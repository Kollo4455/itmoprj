from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ModelForm, ModelSelectionForm

# Create your views here.
from .models import Pickle_model

@login_required
def upload_model(request):
    if request.method == 'POST':
        form = ModelForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            # Обработка после успешной загрузки
    else:
        form = ModelForm(request.user)
    return render(request, 'itmo/upload_model.html',
                  {
                      'form': form,
                      'title': 'Обучение модели',
                   })


def error_404_view(request, exception):
    return render(request, '404.html', {})


@login_required
def model_selection_view(request):
    pickle_path = None  # Инициализация переменной pickle_path

    if request.method == 'POST':
        form = ModelSelectionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Обработка формы при отправке
            excel_file = form.cleaned_data['excel_file']
            user_models = form.cleaned_data['user_models']

            # Получение пути до пикл файла выбранной модели, если модель выбрана
            selected_model = user_models
            if selected_model:
                pickle_path = selected_model.pickle.path if selected_model.pickle else None

            # Ваш код обработки файла и модели

            return render(request, 'itmo/results_page.html',
                          {'pickle_path': pickle_path})  # Передача pickle_path в шаблон результатов
    else:
        form = ModelSelectionForm(user=request.user)

    return render(request, 'itmo/model_selection.html',
                  {
                      'form': form,
                      'title': 'Предсказание',
                  })
