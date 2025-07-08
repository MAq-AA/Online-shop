from django.shortcuts import render
from .models import *
from .forms import *
from .filters import *
from auth_user.models import Profile
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import HttpResponseRedirect
from delivery_staff.models import Order


class CategoryListView(TemplateView):

    def get(self, request, **kwargs):
        context = self.get_context_data()
        if request.GET.get("search") is not None:
            return HttpResponseRedirect(f'http://127.0.0.1:8000/shop/search?search={request.GET.get("search")}')
        return render(request=request, template_name='categoryList.html', context=context)

    def get_cat_and_sub(self):
        list_cat_id = AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).category.all().values_list('id', flat=True)
        cat_and_sub = []
        for i in list_cat_id:
            cat_and_sub.append(Category.object.get(id=i))
            cat_and_sub.append(Subcategory.object.filter(category=i))
        return cat_and_sub

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_and_sub'] = self.get_cat_and_sub()
        context['animal_sort'] = self.kwargs.get('animal_sort', None)
        return context


class ProductListView(TemplateView):
    def get(self, request, **kwargs):
        context = self.get_context_data()
        product = context['all_products']
        if request.GET.get("search") is not None:
            return HttpResponseRedirect(f'http://127.0.0.1:8000/shop/search?search={request.GET.get("search")}')
        elif request.GET.get("order") is not None and request.GET.get("order") != '---------':
            order_list = {
                'mM': Product.objects.filter(animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id, subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by('price'),
                'Mm': Product.objects.filter(animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id, subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by('-price'),
                'population': 1,
                'stars': 1,
            }
            product = order_list[request.GET.get("order")]
        context['filter'] = ProductFilter(request.GET, queryset=product)
        return render(request=request, template_name='productList.html', context=context)

    def post(self, request, **kwargs):
        if request.POST.get("to-basket") is not None:
            return HttpResponseRedirect('http://127.0.0.1:8000/shop/basket/')
        elif request.POST.get("add") is not None:
            Basket.object.get(profile=Profile.object.get(id=self.request.user.id)).products.add(Product.objects.get(id=request.POST.get("add")))
        return self.get(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_sort = AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id
        subcategory = Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id
        context['title'] = Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).title
        context['all_products'] = Product.objects.filter(animal_sort=animal_sort, subcategory=subcategory)
        context['animal_sort'] = self.kwargs.get('animal_sort', None)
        context['subcategory'] = self.kwargs.get('subcategory', None)
        return context


class ProductDetailView(TemplateView):

    def permissions(self):
        profile = Profile.object.get(user=self.request.user)
        product = Product.objects.get(slug=self.kwargs.get('product', None)).id
        permission_to_comm = Basket.object.filter(profile=profile, bought=product).count() and not Feedback.objects.filter(profile=profile, products=product).count()
        permission_to_add = Basket.object.filter(profile=profile, products=product).count()
        return permission_to_comm, permission_to_add

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['form'] = FeedbackForm()
        if request.GET.get("search") is not None:
            return HttpResponseRedirect(f'http://127.0.0.1:8000/shop/search?search={request.GET.get("search")}')
        return render(request=request, template_name='productDetail.html', context=context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        context['form'] = FeedbackForm()
        if request.POST.get("add") is not None:
            Basket.object.get(profile=Profile.object.get(id=self.request.user.id)).products.add(context['product'])
            context['basket_have'] = True
        elif request.POST.get("to-basket") is not None:
            return HttpResponseRedirect('http://127.0.0.1:8000/shop/basket/')
        else:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                Feedback.objects.create(**form.cleaned_data, products=Product.objects.get(slug=self.kwargs.get('product', None)), profile=Profile.object.get(id=self.request.user.id))
                context['permission'] = False

                return HttpResponseRedirect(f"http://127.0.0.1:8000/shop/{self.kwargs.get('animal_sort', None)}"
                                            f"/{self.kwargs.get('subcategory', None)}/{self.kwargs.get('product', None)}")
        return render(request=request, template_name='productDetail.html', context=context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs.get('product', None))
        context['animal_sort'] = AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None))
        context['subcategory'] = Subcategory.object.get(slug=self.kwargs.get('subcategory', None))
        context['list_comments'] = Feedback.objects.filter(products=Product.objects.get(slug=self.kwargs.get('product', None)).id)
        if not self.request.user.id == None:
            context['permission'] = 1
            context['basket_have'] = self.permissions()[1]
        return context


class BasketList(TemplateView):

    def get(self, request, **kwargs):
        context = self.get_context_data()
        if request.GET.get("search") is not None:
            return HttpResponseRedirect(f'http://127.0.0.1:8000/shop/search?search={request.GET.get("search")}')
        return render(request=request, template_name='basketList.html', context=context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if request.POST.get("delete") is not None:
            Basket.object.get(profile=Profile.object.get(user=self.request.user)).products.remove(request.POST.get("delete"))
            return render(request=request, template_name='basketList.html', context=context)
        elif request.POST.get("buy") is not None:
            profile = Profile.object.get(user=self.request.user)
            Order(profile=profile).save()
            ids = Basket.object.get(profile=profile).products.all().values_list('id', flat=True)
            Order.object.filter(profile=profile).latest('profile').products.add(*ids)
            Basket.object.get(profile=profile).products.clear()
            Basket.object.get(profile=profile).bought.add(*ids)
            context['message'] = 'Ваш заказ принят в работу'
            return render(request=request, template_name='basketList.html', context=context)

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(BasketList, self).dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Basket.object.get(profile=Profile.object.get(user=self.request.user)).products.all()
        context['message'] = ''
        return context


class SearchList(TemplateView):
    template_name = 'searchList.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['search'] = request.GET.get("search")
        context['basket'] = Basket.object.get(profile=Profile.object.get(user=self.request.user))
        context['result'] = Product.objects.filter(
                                                   Q(title__icontains=request.GET.get("search")) |
                                                   Q(subcategory__title__icontains=request.GET.get("search")) |
                                                   Q(description__icontains=request.GET.get("search")) |
                                                   Q(shortdescription__icontains=request.GET.get("search")) |
                                                   Q(provider__company__icontains=request.GET.get("search")) |
                                                   Q(animal_sort__title__icontains=request.GET.get("search"))
                                                   )
        product = context['result']
        if request.GET.get("order") is not None:
            order_list = {
                'mM': Product.objects.filter(animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id, subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by('price'),
                'Mm': Product.objects.filter(animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id, subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by('-price'),
                'population': 1,
                'stars': 1,
            }
            product = order_list[request.GET.get("order")]
        context['filter'] = ProductFilter(request.GET, queryset=product)
        return render(request=request, template_name='searchList.html', context=context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        context['search'] = request.GET.get("search")
        if request.POST.get("add") is not None:
            Basket.object.get(profile=Profile.object.get(user=self.request.user)).products.add(request.POST.get("add"))
        elif request.POST.get("to-basket") is not None:
            return HttpResponseRedirect('http://127.0.0.1:8000/shop/basket/')
        context['basket'] = Basket.object.get(profile=Profile.object.get(user=self.request.user))
        context['result'] = Product.objects.filter(
            Q(title__icontains=request.GET.get("search")) |
            Q(subcategory__title__icontains=request.GET.get("search")) |
            Q(description__icontains=request.GET.get("search")) |
            Q(shortdescription__icontains=request.GET.get("search")) |
            Q(provider__company__icontains=request.GET.get("search")) |
            Q(animal_sort__title__icontains=request.GET.get("search"))
        )
        product = context['result']
        if request.GET.get("order") is not None:
            order_list = {
                'mM': Product.objects.filter(
                    animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id,
                    subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by('price'),
                'Mm': Product.objects.filter(
                    animal_sort=AnimalSort.object.get(slug=self.kwargs.get('animal_sort', None)).id,
                    subcategory=Subcategory.object.get(slug=self.kwargs.get('subcategory', None)).id).order_by(
                    '-price'),
                'population': 1,
                'stars': 1,
            }
            product = order_list[request.GET.get("order")]
        context['filter'] = ProductFilter(request.GET, queryset=product)
        return render(request=request, template_name='searchList.html', context=context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = HttpResponseRedirect('http://127.0.0.1:8000/')


class ProductCreateView(CreateView):
    model = Product
    template_name = 'create.html'
    fields = ['slug', 'title', 'img', 'description', 'shortdescription', 'price', 'provider', 'animal_sort', 'subcategory']

