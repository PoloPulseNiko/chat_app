from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("", views.ProfileListView.as_view(), name="profile_list"),
    path("create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path("<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("<int:pk>/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path("<int:pk>/delete/", views.ProfileDeleteView.as_view(), name="profile_delete"),

]
