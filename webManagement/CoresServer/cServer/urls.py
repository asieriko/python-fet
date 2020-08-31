from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fetfiles/results/fet/(?P<file_id>(\d+))$', views.return_result_fet),
    url(r'^fetfiles/results/teacher/(?P<file_id>(\d+))$', views.return_result_teacher),
    url(r'^fetfiles/upload/$', views.upload_files),
    url(r'^fetfiles/results', views.show_results,name='results'),
    url(r'^fetfiles/threads', views.show_threads,name='threads'),
    url(r'^fetfiles/view/(?P<file_id>(\d+))$', views.view_teacher),
    url(r'^fetfiles/assignements$', views.AssignmentFormView,name='asig'),
    url(r'^fetfiles/login/', views.logUserIn, name='login'),
    url(r'^fetfiles/logout/', views.logUserOut, name='logout'),
    url(r'^fetfiles/login_form/', views.loginForm, name='loginForm'),
    url(r'^fetfiles/(?P<computer>(\w+))/(?P<thread>(\w+))$', views.status_page),
    url(r'^fetfiles/(?P<file_id>(\d+))$', views.return_file),
    url(r'^fetfiles/', views.home, name='home'),
]
