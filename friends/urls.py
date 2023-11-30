from django.urls import path
from .views import FriendListView, SendFriendRequestView, RespondToFriendRequestView, FriendRequestListView

urlpatterns = [
    path('friend-list/', FriendListView.as_view(), name='friend-list'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-to-friend-request/<int:pk>/', RespondToFriendRequestView.as_view(), name='respond-to-friend-request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-requests'),
]