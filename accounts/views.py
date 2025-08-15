# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError  # <-- import this

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from spins.models import Spin

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                # authenticate so Django knows the backend
                raw_password = form.cleaned_data.get("password1")
                auth_user = authenticate(request, username=user.username, password=raw_password)
                if auth_user is not None:
                    login(request, auth_user)
                else:
                    # fallback to default backend if needed
                    user.backend = "django.contrib.auth.backends.ModelBackend"
                    login(request, user)
                return redirect("profile", username=user.username)
            except IntegrityError:
                messages.error(request, "There was an account error. Try a different username or email.")
        # if invalid, fall through and re-render with errors
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spins"] = Spin.objects.filter(user=self.object).order_by("-created_at")
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"username": self.request.user.username})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"username": self.request.user.username})
