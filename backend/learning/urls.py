from django.urls import path
from . import views

urlpatterns = [
    path("curriculum/", views.curriculum_list, name="curriculum-list"),
    path("units/<int:unit_id>/", views.unit_detail, name="unit-detail"),
    path("chat/<int:unit_id>/", views.chat_proxy, name="chat-proxy"),
]
