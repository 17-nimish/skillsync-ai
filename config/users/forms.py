from django.contrib.auth.forms import UserCreationForm
from .models import User   # 👈 your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']