from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path(
        "categories/<slug:slug>", views.SpecificCategoryView.as_view(), name="category"
    ),
    path(
        "post-details/<slug:slug>", views.PostDetailView.as_view(), name="post-details"
    ),
    path("search/<slug:slug>", views.PostDetailView.as_view(), name="search-category"),
]
