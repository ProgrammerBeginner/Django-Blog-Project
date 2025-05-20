from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import DetailView, ListView

from .models import Post, Category, Member
from .forms import SignUpForm, LoginForm

# Create your views here.


class HomeView(View):
    def get(self, request):

        try:
            all_posts = Post.objects.all()
            all_categories = Category.objects.all()
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": True,
                    "all_posts": all_posts,
                    "all_categories": all_categories,
                },
            )

        except Post.DoesNotExist:
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": False,
                },
            )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-details.html"


class SignUpView(View):
    def get(self, request):
        sign_up_form = SignUpForm()
        return render(request, "blog/sign-up.html", {"sign_up_form": sign_up_form})

    def post(self, request):
        new_user = SignUpForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(request, "blog/sign-up.html", {"sign_up_form": new_user})


class UserProfileView(View):
    def get(self, request):
        user_id = request.session["user_id"]
        user_info = Member.objects.get(pk=user_id)
        return render(request, "blog/profile.html", {"user": user_info})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "blog/login.html", {"login_form": login_form})

    def post(self, request):
        form_data = LoginForm(request.POST)

        try:
            if form_data.is_valid():
                user_email = form_data.cleaned_data["email"]
                user_password = form_data.cleaned_data["password"]

                user = Member.objects.get(email=user_email)

                if user:
                    if user.password == user_password:
                        request.session["user_id"] = user.id
                        request.session["is_logged_in"] = True

                        return render(
                            request, "blog/all_posts.html", {"is_logged_in": True}
                        )
            return render(request, "blog/login.html", {"login_form": form_data})

        except Member.DoesNotExist:
            return redirect("login")


class LogoutView(View):
    def get(self, request):
        pass


class SpecificCategoryView(View):
    def get(self, request):
        pass
