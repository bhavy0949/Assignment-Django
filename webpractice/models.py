from django.db import models
from django.contrib.auth.models import User

#user profile model

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # email = models.EmailField(_("email address"), blank=True)
    
    def __str__(self):
        return self.user.username #return user name