from django.urls import path

from . import views

urlpatterns = [
    path('tasks/create/', views.CreateTaskView.as_view(), name='create-task'),
    path('tasks/retrieve/<int:user_id>/', views.RetrieveTaskView.as_view(),
         name='retrieve-tasks-by-user'),
    path('tasks/update/<int:pk>/', views.UpdateTaskView.as_view(),
         name='update-task'),
    path('tasks/delete/<int:pk>/', views.DeleteTaskView.as_view(),
         name='delete-task'),
    path('tasks/', views.ListAllTasksView.as_view(), name='list-all-tasks'),
    path("register/", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="user-login"),
]
