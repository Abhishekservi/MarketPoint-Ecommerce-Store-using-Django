from django.urls import path
from core.views import index
from core import *

app_name="core"

urlpatterns =[
    path("test/",index),
]