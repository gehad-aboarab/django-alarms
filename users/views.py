from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterationForm

# Method to register a new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        # Validate the form credentials entered
        if form.is_valid():
            # Save the new user
            form.save()

            # Redirect to the login page and show a success message
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, you can now log in.')
            return redirect('login')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form': form})
