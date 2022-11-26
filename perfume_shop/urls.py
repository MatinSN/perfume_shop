"""perfume_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from perfume_shop import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('men_perfume/', views.men_perfume, name='men_perfume'),
    path('signup/', views.signup),
    path('login/', views.login),
    path('dummy/', views.dummy_fixer),
    path('brands/', views.BrandListView.as_view()),
    path('perfumes/', views.PerfumeListView.as_view()),
    path('rater/', views.temp_rater),
    path('cart/', views.cart),
    path('perfume/<str:id>', views.get_perfume),
    path('payment_request/', views.payment_request),
    path('payment_callback/', views.payment_callback),
    path('addresses/', views.address),
    path('rate_perfume/', views.rate_perfume),
    path('perfume_comments/', views.perfume_comments),
    path('add_comment/', views.add_comment),
    # re_path('^perfumes/(?P<username>.+)/$', views.PerfumeListView.as_view()),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
