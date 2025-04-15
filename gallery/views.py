from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .models import Image
from .forms import ImageForm
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import Image, Comment
from .forms import CommentForm


class GalleryListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'images'
    def get_queryset(self):
        return Image.objects.all().order_by('-uploaded_at')
  



class ImageUploadView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'gallery/image_form.html'
    success_url = reverse_lazy('gallery-list')  

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)



class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('gallery-list')
    template_name = 'gallery/image_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.uploaded_by != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this image.")
        return super().dispatch(request, *args, **kwargs)

    

class ToggleLikeView(View):
    def post(self, request, pk):
        image = Image.objects.get(pk=pk)
        if request.user in image.liked_by.all():
            image.liked_by.remove(request.user)
        else:
            image.liked_by.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('gallery-list')))




class MyFavoritesView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'gallery/my_favorites.html'
    context_object_name = 'images'

    def get_queryset(self):
        return self.request.user.favorite_images.all()




class NewsFeedView(ListView):
    model = Image
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'images'

    def get_queryset(self):
        return Image.objects.exclude(uploaded_by=self.request.user).order_by('-uploaded_at')


# gallery/views.py
class ProfileView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'gallery/profile.html'
    context_object_name = 'images'

    def get_queryset(self):
        return Image.objects.filter(uploaded_by=self.request.user).order_by('-uploaded_at')



class ImageDetailView(DetailView):
    model = Image
    template_name = 'gallery/image_detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = self.object
            comment.author = request.user
            comment.save()
            return redirect('image-detail', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
