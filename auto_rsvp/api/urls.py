from django.urls import path
from .views import GroupListAPIView, GroupDetailAPIView

urlpatterns = [
    path('groups/', GroupListAPIView.as_view(), name='group-list'),
    path('groups/<int:group_id>/',
         GroupDetailAPIView.as_view(), name='group-detail'),
]
