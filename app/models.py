from django.db import models
from django.utils.timezone import now

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "users" 
        managed = True  

    def __str__(self):
        return self.email
