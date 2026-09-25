from accounts.views import login, logout
from django.urls import path

app_name = "accounts"

urlpatterns = [
	path("login/", login, name="login"),
	path("logout/", logout, name="logout"),
]