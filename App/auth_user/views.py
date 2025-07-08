from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.models import User, Group
from django.views.generic import *
from django.utils.decorators import method_decorator
from shop.models import Basket
from news.models import Post
class RegisterView(TemplateView):

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.groups.add(Group.objects.get(name='Consumer'))
            Profile(user=user).save()
            Basket(profile=Profile.object.get(user=user)).save()
            messages.success(request, message=f'Ваш аккаунт создан:можно войти на сайт, {username}.')
            return redirect('login')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = UserRegisterForm()
            logout(request)
        return render(request=request, template_name='users/register.html', context=context)

    def get(self, request, **kwargs):
        logout(request)
        context = self.get_context_data(**kwargs)
        context['form'] = UserRegisterForm()
        return render(request=request, template_name='users/register.html', context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(TemplateView):

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['profile'] = Profile.object.get(user=self.request.user)
        return render(request=request, template_name='users/profile.html', context=context)

    def post(self, request, **kwargs):
        if request.POST.get("logout") is not None:
            pass
        return redirect('logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def logout_view(request):
    logout(request)
    context = {
        'news_list': Post.objects.filter(type='1')
        }
    return render(request, template_name='../../news/templates/newsList.html', context=context)


class ChangeView(UpdateView):
    model = User
    template_name = 'users/change.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('profile')


class DeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('register')
