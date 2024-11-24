from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),
    path('', include('app_user.urls')),
    path('', include('app_product.urls')),

    path('password-reset/', PasswordResetView.as_view(template_name='app_user/password-reset.html'),
         name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='app_user/reset-password-done.html'),
         name='password_reset_done'),
    path('reset/<token>/<uidb64>/',
         PasswordResetConfirmView.as_view(template_name='app_user/reset-password-confirmation.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='app_user/reset-password-complited.html')),

    # social oauth
    path('social-auth/', include('social_django.urls', namespace='social')),

]
