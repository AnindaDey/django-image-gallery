from django.urls import path
from .views import GalleryListView, ImageUploadView, ImageDeleteView,ToggleLikeView,MyFavoritesView,NewsFeedView,ImageDetailView,CustomSignupView,MyProfileView

urlpatterns = [
    path('gallery_list/', GalleryListView.as_view(), name='gallery-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('delete/<int:pk>/', ImageDeleteView.as_view(), name='image-delete'),
    path('image/<int:pk>/like/', ToggleLikeView.as_view(), name='image-like'),
    path('favorites/', MyFavoritesView.as_view(), name='my-favorites'),
    path('news-feed/', NewsFeedView.as_view(), name='news-feed'),
    path('toggle-like/<int:pk>/', ToggleLikeView.as_view(), name='toggle-like'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
   
]