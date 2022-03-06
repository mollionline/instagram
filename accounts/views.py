from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from accounts.forms import UserCreationForm, ProfileCreateForm

# Create your views here.
from django.views import View

from accounts.models import Profile


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html', context={
            'next': request.GET.get('next')
        })

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_page = request.GET.get('next')
        if user is not None:
            login(request, user)
            if next_page is not None:
                return redirect(next_page)
            return redirect('/')
        # elif user is None:
        #     User = get_user_model()
        #     email_num = User.objects.all().filter(email__iexact=username)
        #     if email_num:
        #         username = email_num[0].username
        #         user = authenticate(username=username, password=password)
        #         login(request, user)
        #         if next_page is not None:
        #             return redirect(next_page)
        #         return redirect('/')
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        profile_form = ProfileCreateForm()
        genders = Profile.GENDER
        return render(request, 'registration/registration.html',
                      context={'form': form,
                               'profile_form': profile_form,
                               'genders': genders})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        profile_form = ProfileCreateForm(request.POST, request.FILES)
        genders = Profile.GENDER
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('/')
        return render(request, 'registration/registration.html',
                      context={'form': form,
                               'profile_form': profile_form,
                               'genders': genders})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile/profile.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0
