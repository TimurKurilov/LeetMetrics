from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.startpage, name="startpage"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]
 