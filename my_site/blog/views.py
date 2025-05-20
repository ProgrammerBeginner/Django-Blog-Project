from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import DetailView, ListView

from .models import Post, Category, Member
from .forms import SignUpForm, UserProfileForm, LoginForm, ChangePasswordForm

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
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )

        except Post.DoesNotExist:
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": False,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_logged_in"] = self.request.session.get("is_logged_in")


class SignUpView(View):
    def get(self, request):
        sign_up_form = SignUpForm()
        return render(
            request,
            "blog/sign-up.html",
            {
                "sign_up_form": sign_up_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        new_user = SignUpForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(
                request,
                "blog/sign-up.html",
                {
                    "sign_up_form": new_user,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class UserProfileView(View):
    def get(self, request):
        user_id = request.session["user_id"]
        user = Member.objects.get(pk=user_id)
        user_profile_form = UserProfileForm(instance=user)
        return render(
            request,
            "blog/profile.html",
            {
                "user_profile_form": user_profile_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        user_id = request.session["user_id"]
        user = Member.objects.get(pk=user_id)
        user_profile_form = UserProfileForm(request.POST, instance=user)

        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect("home")
        else:
            return render(
                request,
                "blog/profile.html",
                {
                    "user_profile_form": user_profile_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


# change_password_form
class ChangePasswordView(View):
    def get(self, request):
        change_password_form = ChangePasswordForm()
        return render(
            request,
            "blog/change-password.html",
            {
                "change_password_form": change_password_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        user_id = request.session["user_id"]
        user = Member.objects.get(pk=user_id)

        if change_password_form.is_valid():

            if user.password == request.POST["password"]:
                if request.POST["confirm_password"] == request.POST["new_password"]:
                    user.password = request.POST["new_password"]
                    user.save()
                    return redirect("home")

                else:
                    return render(
                        request,
                        "blog/change-password.html",
                        {
                            "change_password_form": change_password_form,
                            "is_logged_in": request.session.get("is_logged_in"),
                            "error-message": "New Password Incorrect!",
                        },
                    )
            else:
                return render(
                    request,
                    "blog/change-password.html",
                    {
                        "change_password_form": change_password_form,
                        "is_logged_in": request.session.get("is_logged_in"),
                        "error-message": "Your Password Incorrect!",
                    },
                )

        else:
            return render(
                request,
                "blog/change-password.html",
                {
                    "change_password_form": change_password_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(
            request,
            "blog/login.html",
            {
                "login_form": login_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

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
                            request,
                            "blog/all_posts.html",
                            {"is_logged_in": True},
                        )
            return render(request, "blog/login.html", {"login_form": form_data})

        except Member.DoesNotExist:
            return redirect("login")


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("home")


class SpecificCategoryView(View):
    def get(self, request):
        pass
