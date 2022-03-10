from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel

from django.views.generic import DetailView, UpdateView, ListView
from typing import Dict
from urllib.parse import urlencode

from django.db.models import Q
from accounts.forms import UserCreationForm, ProfileCreateForm, UserChangeForm, ProfileChangeForm
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel

from accounts.forms import UserCreationForm, ProfileCreateForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm, FollowToSomeoneForm

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
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/accounts/login/')


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

    def get_context_data(self, **kwargs):
        posts = self.object.posts.order_by('-created_at')
        kwargs['posts'] = posts
        return super().get_context_data(**kwargs)


class UserFollowedToSomeoneView(DetailView):
    model = get_user_model()
    template_name = 'partial/followed_to_someone.html'
    context_object_name = 'user_obj'


class ProfileFollowedUsersView(DetailView):
    model = get_user_model()
    template_name = 'partial/profile_followed_users.html'
    context_object_name = 'user_obj'


class UserProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile/user_profile_update.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
            kwargs['genders'] = Profile.GENDER
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        context['genders'] = Profile.GENDER
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


def search(request):
    sterm = request.GET.get('search1', None)
    if sterm == None:
        return redirect('list_post')

    else:
        user = Profile.objects.filter(Q(user__username__iexact=sterm) |
                                      Q(user__first_name__iexact=sterm) |
                                      Q(user__email__iexact=sterm))

    return render(request, 'partial/search.html', {'q': user})


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'registration/change_password.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)


class FollowProfileView(UpdateView):
    model = get_user_model()
    form_class = FollowToSomeoneForm
    template_name = 'profile/profile.html'
    context_object_name = 'user_obj'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            profile = self.kwargs.get('pk')
            user_followed = self.request.user
            user_followed.profile.followers.add(profile)
            url = reverse('profile', kwargs={
                'pk': profile
            })
            return HttpResponseRedirect(url)
        return render(request, self.template_name, context={'form': form})

