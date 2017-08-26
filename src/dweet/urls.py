from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create/$', create_dweet_view, name="create_dweet_view"),
    url(r'^add/$', add_dweet, name="add_dweet"),
    url(r'^(?P<dweet_id>\d+)/$', delete_dweet, name="delete_dweet"),
    url(r'^all/$', get_dweets, name="get_dweets"),
    url(r'^comment/add/$', add_comment, name="add_comment"),
    url(r'^comment/(?P<dweet_id>\d+)/$', get_comments, name="get_comments"),
    url(r'^like/$', like_dweet, name="like_dweet"),
]
