from django.conf.urls import url

import views

urlpatterns = [
    url(r'(?P<name>[A-Za-z0-9]+)$', views.register_url),
    url(r'', views.register_url_all),
]
