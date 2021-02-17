from django.conf.urls import url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'WordLearn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^left/$', views.left),
    url(r'^right/$', views.right),
    url(r'^translate/$', views.translate),
]
