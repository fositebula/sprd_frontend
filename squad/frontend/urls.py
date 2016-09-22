from django.conf.urls import url

from . import views

slug_pattern = '[a-z0-9_.-]+'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(%s)/$' % slug_pattern, views.group, name='group'),
    url(r'^(%s)/(%s)/$' % ((slug_pattern,) * 2), views.project, name='project'),
]
