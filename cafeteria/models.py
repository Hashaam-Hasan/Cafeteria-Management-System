from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.




class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  # Adjusted to remove default=None as it's not needed
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    
    email = models.CharField(max_length=200, null=True, unique=True)
    f_name = models.CharField(max_length=200, null=True)
    l_name = models.CharField(max_length=200, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username if self.user else''
