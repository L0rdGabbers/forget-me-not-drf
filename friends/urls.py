from django.urls import path
from .views import FriendListView, FriendDetailView, SendFriendRequestView, RespondToFriendRequestView, FriendRequestListView

urlpatterns = [
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('friends/<int:pk>/', FriendDetailView.as_view(), name='friend-list'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-requests/<int:pk>/', RespondToFriendRequestView.as_view(), name='respond-to-friend-request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-requests'),
]