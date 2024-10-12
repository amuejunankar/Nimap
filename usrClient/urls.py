from django.urls import path
from .views import (
    home,
    loginn,
    logout_view,
    user_dashboard,
    ClientListCreateView,
    ClientDetailView,
    ProjectCreateForClientView,
    ProjectDetailView,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginn, name='loginn'),
    path('logout/', logout_view, name='logout'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),

    # Client URLs
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),

    # Project URLs for a specific client
    path('clients/<int:id>/projects/', ProjectCreateForClientView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
