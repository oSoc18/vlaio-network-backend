from django.db import models
from django.contrib.auth.models import User


class Roles:
    PENDING = "pending"
    USER = "user"
    ADMIN = "admin"


CASES = {
    # (is_active, is_superuser)
    (False, False): Roles.PENDING,
    (False, True): Roles.PENDING,
    (True, False): Roles.USER,
    (True, True): Roles.ADMIN
}


class ProxyUser(User):
    class Meta:
        proxy = True
    
    def save(self, *a, **k):
        self.username = self.email
        User.save(self, *a, **k)
    
    @property
    def role(self):
        return CASES[(self.is_active, self.is_superuser)]

    @role.setter
    def role(self, value):
        if value == Roles.PENDING:
            self.is_active = False
            return
        else:
            self.is_active = True
        if value == Roles.ADMIN:
            self.is_superuser = True
        else:
            self.is_superuser = False
