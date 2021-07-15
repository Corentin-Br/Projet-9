"""LitrReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('posts', views.SelfFeedView.as_view(), name='posts'),
    path('follow/', views.FollowView.as_view(), name='follows'),
    path('ticket-creation/', views.TicketCreate.as_view(), name='ticket-create'),
    path('review-creation/', views.ReviewAndTicketCreate.as_view(), name='review-create'),
    path('review-creation/<int:pk>', views.ReviewCreate.as_view(), name='review-create-with-ticket'),
    path('review-edit/<int:pk>', views.ReviewUpdate.as_view(), name='edit-review'),
    path('review-delete/<int:pk>', views.ReviewDelete.as_view(), name='remove-review'),
    path('ticket-edit/<int:pk>', views.TicketUpdate.as_view(), name='edit-ticket'),
    path('ticket-delete/<int:pk>', views.TicketDelete.as_view(), name='remove-ticket'),
]
