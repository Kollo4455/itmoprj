import datetime

from django import forms
from .models import Pickle_model
from django.core.files.base import ContentFile
import pickle

import numpy as np
import pandas as pd
from sklearn import ensemble
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error, mean_absolute_error, mean_squared_log_error, explained_variance_score
from sklearn.model_selection import train_test_split

from fedot import Fedot
from fedot.core.data.data import InputData
from fedot.core.data.data_split import train_test_data_setup
from fedot.core.repository.tasks import Task, TaskTypesEnum



def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

class ModelForm(forms.ModelForm):
    class Meta:
        model = Pickle_model
        fields = ['name']  # Поля, которые будут отображаться в форме

    # Дополнительные поля для формы (не из модели)
    excel_file = forms.FileField(label='Upload Excel File')


    def __init__(self,user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

    def save(self, user,name, commit=True):
        instance = super(ModelForm, self).save(commit=False)
        instance.user = user


        # Обработка загруженного Excel файла
        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            # Обработка файла (ваш код)
            data = pd.read_csv(excel_file)

            features_df = data.drop(axis=1, columns=['target'])
            target_df = data['target']

            data = InputData.from_dataframe(features_df,
                                            target_df,
                                            task=Task(TaskTypesEnum.regression))
            train, test = train_test_data_setup(data)

            SEED = 42
            TIMEOUT = 5
            PROBLEM = 'regression'

            # По стандарту используються весь процессор для вычисления
            # n_jobs (int) – num of n_jobs for parallelization (set to -1 to use all cpu’s). Defaults to -1
            # https://fedot.readthedocs.io/en/latest/api/api.html
            model = Fedot(problem=PROBLEM, seed=SEED, timeout=TIMEOUT)
            best_pipeline = model.fit(features=train, target='target')
            prediction = model.predict(features=test)




            content = pickle.dumps(model)
            fid = ContentFile(content,name=f"pickle-{datetime.datetime.now().strftime('%m-%d-%y %H-%M-%S')}.pkl")
            instance.pickle = fid
            fid.close()


            mse = mean_squared_error(test.target, prediction)
            instance.mse = mse
            r2 = r2_score(test.target, prediction)
            instance.r2 = r2
            median = median_absolute_error(test.target, prediction)
            instance.median = median
            mean = mean_absolute_error(test.target, prediction)
            instance.mean = mean
            msle = mean_squared_log_error(test.target, prediction)
            instance.msle = msle
            evs = explained_variance_score(test.target, prediction)
            instance.evs = evs
            mape = mean_absolute_percentage_error(test.target, prediction)
            instance.mape = mape


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
