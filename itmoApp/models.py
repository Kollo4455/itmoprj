from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'pickle/user_{0}/{1}'.format(instance.user.id, filename)

class Pickle_model(models.Model):
    user = models.ForeignKey(User, related_name='upload_file', on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    pickle = models.FileField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
