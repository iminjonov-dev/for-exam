from django.urls import path, include
from .views import user_logout, UserRegistration, update_account
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='app_user/login.html'), name='login'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    # path('account#/?/<int:user_id>/', AccountUpdateView.as_view(), name='account'),
    path('update-account/', update_account, name='account'),

]
