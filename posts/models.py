from django.db import models

class Post(models.Model):
    recruiter = models.ForeignKey('authentication.Recruiter', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.JSONField()  
    deadline = models.DateField()
    def _str_(self):
        return self.title