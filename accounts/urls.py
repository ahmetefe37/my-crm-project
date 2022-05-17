from re import template
from tempfile import tempdir
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # homepage 
    path('', views.home,name='homeurl'),
    # product page
    path("product/",views.product,name='producturl'),
    # customer page
    path("customer/<str:pk_customer>",views.customer,name="customerurl"),
    # user page
    path("user/",views.userPage,name="userurl"),
    # account settings page
    path("account/",views.account_set,name="accounturl"),

    # order CRUD Operations
    path("create_order/<str:pk_customer>",views.create_order,name="createorderurl"),
    path("update_order/<str:pk_order>",views.update_order,name="updateorderurl"),
    path("delete_order/<str:pk_order>",views.delete_order,name="deleteorderurl"),

    # login-registration pages
    path("register/",views.registerPage,name="registerurl"),
    path("login/",views.loginPage,name="loginurl"),
    path("logout/",views.logoutUser,name="logouturl"),

    # password reset pages
    path("reset_password/",
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name = "reset_password"),
    path("reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), 
        name = "password_reset_done"),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"),
        name = "password_reset_confirm" ),
    path("reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"),
        name = "password_reset_complete"),
]

