from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.JSONField()  
    deadline = models.DateField()
    company = models.CharField(max_length=100)
    def _str_(self):
        return self.title