from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts import views as accountviews
from dashboard import views as dashboardviews
from leetcode.services.snapshot import dashboard_data


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", accountviews.startpage, name="startpage"),
    path('register/', accountviews.RegisterView.as_view(), name='register'),
    path('login/', accountviews.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('dashboard/<str:username>/', dashboardviews.dashboard, name='dashboard'),
    path("api/dashboard-data/<str:username>/", dashboard_data, name="dashboard-data"),
]
 