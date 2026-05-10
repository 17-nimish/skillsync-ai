from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm


# ================================
# 🔐 SIGNUP VIEW
# ================================
def signup(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Account created successfully! 🎉 Please login.")

            return redirect('login')

        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ================================
# 🔐 LOGIN VIEW (CUSTOM)
# ================================
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ SUCCESS POPUP
            messages.success(request, "Login Successful! 🚀")

            return redirect('/')

        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, 'login.html')