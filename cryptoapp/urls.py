from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.userlogout, name="logout"),
    path("profile/", views.afterloginpage, name="profile"),
    path("kyc/", views.kyc, name="kyc"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path("buy/<str:symbol>/", views.buy_view, name="buy"),
    path("get_live_prices/", views.get_live_prices, name="get_live_prices"),
    path("sell_coin/", views.sell_coin, name="sell_coin"),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
