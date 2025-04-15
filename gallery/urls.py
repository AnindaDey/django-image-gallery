from django.urls import path
from .views import GalleryListView, ImageUploadView, ImageDeleteView

urlpatterns = [
    path('', GalleryListView.as_view(), name='gallery-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('delete/<int:pk>/', ImageDeleteView.as_view(), name='image-delete'),
]