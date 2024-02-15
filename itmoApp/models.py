from django.db import models
from django.contrib.auth.models import User


# Create your models here.


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'pickle/user_{0}/{1}'.format(instance.user.id, filename)


class PickleModel(models.Model):
    user = models.ForeignKey(User, related_name='upload_file', on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    pickle = models.FileField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    mse = models.CharField(max_length=100)
    r2 = models.CharField(max_length=100)
    mean = models.CharField(max_length=100)
    median = models.CharField(max_length=100)
    msle = models.CharField(max_length=100)
    evs = models.CharField(max_length=100)
    mape = models.CharField(max_length=100)

    def __str__(self):
        return self.name
