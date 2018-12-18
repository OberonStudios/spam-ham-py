from django.urls import include, path

from . import views

urlpatterns = [
    # path('stripe_paid/<int:pk>', views.stripe_paid, name='stripe_paid'),
    path('', views.base_posts.as_view(), name='base_posts'),
    path('dashboard', views.base_dashboard.as_view(), name='base_dashboard'),
    path('post/<int:pk>/', views.base_post.as_view(), name='base_post'),
    path('post/add', views.base_post_add, name='base_post_add'),
    path('post/<int:pk>/edit/', views.base_post_edit, name='base_post_edit'),
    path('post/(<int:pk>/comment/', views.base_comment, name='base_comment'),
    path('accounts/register', views.base_auth_reg, name='base_auth_reg'),
    path('', include('social_django.urls', namespace='social')),

]
