from django.db import models
from django.contrib.auth.models import User


class ProxyUser(User):
    class Meta:
        proxy = True
    
    def save(self, *a, **k):
        self.username = self.email
        User.save(self, *a, **k)
