from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

# Create your views here.


class SignUpView(CreateView):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
        return render(request, 'signup.html', {'form': form})
    

