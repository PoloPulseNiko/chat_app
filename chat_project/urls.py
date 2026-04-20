"""
URL configuration for chat_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect


def home(request):
    return redirect('/rooms/')


urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('notifications/', include('notifications_app.urls')),
    path('rooms/', include('rooms_app.urls')),
    path('profiles/', include('profiles_app.urls')),
    path('messages/', include('messages_app.urls')),  # for delete
    path('staff-panel/', include('staff_panel_app.urls')),

]


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


handler404 = custom_404
handler500 = custom_500
