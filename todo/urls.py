from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/', views.todo, name='todo'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('complete/<int:id>/', views.toggle_complete, name='complete'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
]
