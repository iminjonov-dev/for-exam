from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.shortcuts import render, redirect
from app_user.forms import UserRegistrationForm, UpdateAccountForm
from app_user.models import UserModel

User = get_user_model()


class UserRegistration(CreateView):
    model = User
    template_name = 'app_user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect('categories')


# class AccountUpdateView(UpdateView):
#     model = User
#     template_name = 'app_user/account.html'
#     form_class = UserAccountUpdateForm
#     success_url = reverse_lazy('categories')


# def AccountUpdateView(request):
#     return render(request, 'app_user/account.html')

# @method_decorator(login_required, name='dispatch')
# class AccountUpdateView(UpdateView):
#     template_name = "app_user/account.html"
#     success_url = reverse_lazy("users:account")
#     model = UserModel
#     form_class = UserAccountUpdateForm
#
#
#     def form_valid(self, form: BaseModelForm) -> HttpResponse:
#         data = form.cleaned_data
#         user = form.save(commit=False)
#
#         if data.get("password"):
#             user.set_password(data["password"])
#
#         if user != self.request.user:
#             return super().form_invalid(form)
#
#         user.save()
#         return super().form_valid(form)
#
#     # def get_object(self, queryset=None):
#     #     user_id = self.kwargs.get(self.pk_url_kwarg)
#     #     return get_object_or_404(User, pk=user_id)


@login_required
def update_account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = UpdateAccountForm(instance=request.user)

    return render(request, 'app_user/account.html', {'form': form})
