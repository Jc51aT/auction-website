from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:listing_id>/',views.auction, name='auction'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:listing_categories>', views.category, name='category'),
    path('watchlist/', views.watchlist, name='watchlist'),
    re_path(r'(?P<listing_id>[0-9]*)/watchlist_ajax/$',views.watchlist_ajax),
    re_path(r'(?P<listing_id>[0-9]*)/watchlist_remove_ajax/$',views.watchlist_remove_ajax),
    re_path(r'(?P<listing_id>[0-9]*)/comment_ajax/$',views.comment_ajax),
    
]