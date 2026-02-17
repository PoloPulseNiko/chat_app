from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, "profiles_app/profile_list.html", {"profiles": profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, "profiles_app/profile_detail.html", {"profile": profile})

def profile_create(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile_list")
    else:
        form = ProfileForm()
    return render(request, "profiles_app/profile_form.html", {"form": form})

def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles_app/profile_form.html", {"form": form})
