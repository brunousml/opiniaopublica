from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^vote/(?P<register_id>[0-9]+)/(?P<vote_id>[0-9]+)/$', views.vote, name='vote'),
	url(r'^isvalid/(?P<register_id>[0-9]+)/$', views.validation_id, name='validation_id'),
	url(r'^api/impeachment/all/$', views.all_votes, name='all_votes'),
	url(r'^api/impeachment/counted_votes/$', views.counted_votes, name='counted_votes'),
]