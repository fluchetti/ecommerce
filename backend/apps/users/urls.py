from django.urls import path
from apps.users.views import ListUsers, DetailDeleteUpdateUser, UserSignupView, ListUserProducts, ChangeUserPassword, DeleteUserProfileImage
urlpatterns = [
    path('', ListUsers.as_view(), name='list_users'),
    path('signup', UserSignupView.as_view(), name='signup_user'),
    path('posts', ListUserProducts.as_view(), name='user_posts'),
    path('change_password', ChangeUserPassword.as_view(), name='change_password'),
    path('delete_profile_image', DeleteUserProfileImage.as_view(),
         name='delete_profile_image'),
    path('<str:slug>', DetailDeleteUpdateUser.as_view(), name='detail_user'),
]
