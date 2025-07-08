from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from .models import Post
from shop.models import Product


class NewsListView(TemplateView):
    def get(self, request, **kwargs):
        context = self.get_context_data()
        if request.GET.get("search") is not None:
            return HttpResponseRedirect(f'http://127.0.0.1:8000/shop/search?search={request.GET.get("search")}')
        return render(request=request, template_name='newsList.html', context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = Post.objects.filter(type='1')
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'newsDetail.html'


class NewsCreateView(CreateView):
    model = Post
    template_name = 'newsCreate.html'
    fields = ['title', 'img', 'description']


class NewsUpdateView(UpdateView):
    model = Post
    template_name = 'newsUpdate.html'
    fields = ['title', 'img', 'description']
    success_url = reverse_lazy('News_list')


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'newsDelete.html'
    success_url = reverse_lazy('News_list')


class SearchList(TemplateView):
    template_name = 'searchList.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['result'] = Product.objects.filter(
                                                   Q(title__icontains=request.GET.get("search")) |
                                                   Q(subcategory__title__icontains=request.GET.get("search")) |
                                                   Q(description__icontains=request.GET.get("search")) |
                                                   Q(shortdescription__icontains=request.GET.get("search")) |
                                                   Q(provider__company__icontains=request.GET.get("search")) |
                                                   Q(animal_sort__title__icontains=request.GET.get("search"))
                                                   )
        return render(request=request, template_name='searchList.html', context=context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        request.GET.get("s")

        return render(request=request, template_name='searchList.html', context=context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
