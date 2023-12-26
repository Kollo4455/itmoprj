import datetime

from django import forms
from .models import Pickle_model
from django.core.files.base import ContentFile
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
import re
from sklearn.metrics import mean_squared_log_error
from sklearn.model_selection import train_test_split
import torch
import matplotlib.pyplot as plt
from lightautoml.automl.presets.tabular_presets import TabularAutoML, TabularUtilizedAutoML
from lightautoml.tasks import Task
from sklearn import ensemble
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes


class ModelForm(forms.ModelForm):
    class Meta:
        model = Pickle_model
        fields = ['name']  # Поля, которые будут отображаться в форме

    # Дополнительные поля для формы (не из модели)
    excel_file = forms.FileField(label='Upload Excel File')


    def __init__(self,user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

    def save(self, user, commit=True):
        instance = super(ModelForm, self).save(commit=False)
        instance.user = user


        # Обработка загруженного Excel файла
        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            # Обработка файла (ваш код)
            data = pd.read_csv(excel_file)
            X_train, X_test = train_test_split(data, test_size=0.2, random_state=13)

            params = {
                "n_estimators": 500,
                "max_depth": 4,
                "min_samples_split": 5,
                "learning_rate": 0.01,
                "loss": "squared_error",
            }

            reg = ensemble.GradientBoostingRegressor(**params)
            reg.fit(X_train[X_train.columns[:-1]], X_train['target'])

            mse = mean_squared_error(X_test['target'], reg.predict(X_test[X_test.columns[:-1]]))

            N_THREADS = 1  # threads cnt for lgbm and linear models
            N_FOLDS = 2  # folds cnt for AutoML
            # RANDOM_STATE = 42 # fixed random state for various reasons
            # TEST_SIZE = 0.2 # Test size for metric check
            TIMEOUT = 12  # Time in seconds for automl run

            task = Task('reg', loss='mse', metric='mse')

            roles = {
                'target': 'target',
                'drop': ['Id'],
            }

            cnt_trained = 0
            results = []
            rs_list = list(range(0, 2))
            for it, rs in enumerate(rs_list):
                automl = TabularAutoML(task=task,
                                       timeout=TIMEOUT,
                                       cpu_limit=N_THREADS,
                                       reader_params={'n_jobs': N_THREADS, 'cv': N_FOLDS, 'random_state': rs})
                oof_pred = automl.fit_predict(X_train, roles=roles)

                test_pred = automl.predict(X_test)
                cnt_trained += 1

                if it == 0:
                    oof_pred_full = oof_pred.data[:, 0].copy()
                    test_pred_full = test_pred.data[:, 0].copy()
                else:
                    oof_pred_full += oof_pred.data[:, 0]
                    test_pred_full += test_pred.data[:, 0]

                mse_usual = mean_squared_error(X_test['target'].values, test_pred.data[:, 0])
                mse_full = mean_squared_error(X_test['target'].values, test_pred_full / cnt_trained)
                results.append((mse_usual, mse_full, mse_full - mse_usual))

            content = pickle.dumps(automl)
            fid = ContentFile(content,name=f"pickle-{datetime.datetime.now()}")
            instance.pickle = fid
            fid.close()

            mse = mean_squared_error(X_test['target'].values, automl.predict(X_test).data[:, 0])
            instance.mse = mse

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
