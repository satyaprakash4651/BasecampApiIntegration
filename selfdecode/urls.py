from django.conf.urls import url, include
from django.contrib import admin

from todoapp.views import CustomLoginView, index, todoadd

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^todo/add/$', todoadd),
    url(r'^accounts/login/$', CustomLoginView.as_view(), name='account_login'),
    url(r'^accounts/', include('allauth.urls')),
]
