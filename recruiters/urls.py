from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_recruiter),
    path('list/', views.list_recruiters),
    path('<int:recruiter_id>/find/', views.retrieve_recruiter),
    path('<int:recruiter_id>/update/', views.update_recruiter),
    path('<int:recruiter_id>/delete/', views.delete_recruiter),
    path('<int:recruiter_id>/candidates_applys_ToRecruter/', views.candidates_applys_ToRecruter),

]
