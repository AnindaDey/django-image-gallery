from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Image
from .forms import ImageForm

class GalleryListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'images'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(uploaded_by=self.request.user)


class ImageUploadView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'gallery/image_form.html'
    success_url = reverse_lazy('gallery-list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    template_name = 'gallery/image_confirm_delete.html'
    success_url = reverse_lazy('gallery-list')

    def test_func(self):
        image = self.get_object()
        return self.request.user == image.uploaded_by