from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from spins.models import Spin

CustomUser = get_user_model()

# Registration View


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)  # include FILES
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError as e:
                messages.error(request, "There was an account error. Try a different username or email.")
                return render(request, "accounts/register.html", {"form": form})
            login(request, user)
            return redirect("profile", username=user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# Profile View 
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser  
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username' 
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spins'] = Spin.objects.filter(user=self.object).order_by('-created_at')
        return context


# Edit Profile View
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

# Login View
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


