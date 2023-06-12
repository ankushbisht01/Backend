from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('tour/', views.TourView.as_view()),
    path('tour/<int:pk>/', views.SingleTourView.as_view()),
    path('tour/<int:pk>/update/', views.SingleTourView.as_view()),
    path('tour/<int:pk>/delete/', views.SingleTourView.as_view()),
    
    path('rating/<int:pk>/', views.SingleRatingView.as_view()),
    


]