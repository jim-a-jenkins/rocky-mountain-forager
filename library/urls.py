from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from library.views import account
from library.views import library
from library.views import register
from library.views import plant_detail
from library.views import images
from library.views import image
from library.views import plants
from library.views import plant

app_name = "library"

urlpatterns = [
    path("library/", library, name="library"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("account/", account, name="account"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("library:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("library:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("library:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("register/", register, name="register"),
    path("library/<slug:plant>/", plant_detail, name="plant_detail"),
    # api
    path("api/v1/images/", images, name="images"),
    path("api/v1/images/<int:pk>", image, name="image"),
    path("api/v1/plants/", plants, name="plants"),
    path("api/v1/plants/<int:pk>", plant, name="plant"),
]
