from django import forms

from .models import Member, Comment


class SignUpForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = Member
        exclude = ("joined_date", "slug")


class LoginForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    password = forms.CharField(
        label="Your Password", widget=forms.PasswordInput, min_length=8
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
