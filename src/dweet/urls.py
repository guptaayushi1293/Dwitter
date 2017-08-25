from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create/$', create_dweet_view, name="create_dweet_view"),
    url(r'^add/$', add_dweet, name="add_dweet"),
    url(r'^(?P<dweetId>\d+)$', delete_dweet, name="delete_dweet"),
    url(r'^all/$', get_dweets, name="get_dweets"),
]
