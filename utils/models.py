from django.db import models

class Intern(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    skills = models.JSONField()
    education = models.JSONField()

    def _str_(self):
        return self.name
