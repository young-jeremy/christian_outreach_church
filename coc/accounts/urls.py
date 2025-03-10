from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('', views.accounts, name='accounts'),
    path('logout/', views.logout, name='logout'),
    path('accounts_settings_and_privacy/', views.accounts_settings_and_privacy, name='accounts_settings_and_privacy'),
    path('activity_log/', views.activity_log, name='activity_log'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('contact_support/', views.contact_support,name='contact_support'),
    path('upload_profile/', views.upload_profile_photo, name='upload_profile'),
    path('register', views.register_view, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('account_settings/community/', views.community_list, name='community'),
    # path('view_notifications/', views.view_notifications, name='view_notification'),
    path('view_notifications/mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('account_settings/create_community/', views.create_community, name='create_community'),
    path('community_list/', views.community_list, name='community_list'),
    path('community_details/<int:community_id>/', views.community_details, name='community_details'),
    path('join_community/', views.join_community, name='join_community'),
    path('apps/', views.apps, name='apps'),
#    path('notifications/', views.view_notifications, name='view_notifications'),
#    path('add_subscriptions/', views.toggle_subscription, name='add_subscriptions'),
    path('profile/', views.profile, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check_nudity/', views.check_for_nudity, name='check_nudity'),
#    path('channels_list/', views.channels, name='channel_list'),
    # N
#    path('notifications/', views.view_notifications,name='view_notifications'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('register_new_user/', views.register_new_user, name='register_new_user'),
    path('account_settings/', views.account_settings, name='settings'),


    # P
    path('password/', views.password_reset_request, name='password_reset'),

    # U
    path('update_profile/', views.update_profile, name='update_profile'),
    path('password_reset/', views.password_reset_request, name='password_reset'),

    # S
    path('signup/', views.signup_view, name='signup'),
    path('password_change/', views.change_password, name='password_change'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),

    path('directory/', views.MemberDirectoryView.as_view(), name='directory'),
    path('member/profile/<slug:slug>/', views.MemberProfileView.as_view(), name='member_profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),

    path('member_list/', views.MemberListView.as_view(), name='member_list'),

    path('accounts_settings_and_privacy/', views.accounts_settings_and_privacy, name='accounts_settings_and_privacy'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('security_settings/', views.security_settings, name='security_settings'),
    path('privacy_settings/', views.privacy_settings, name='privacy_settings'),
    path('ministry_preferences/', views.ministry_preferences, name='ministry_preferences'),
    path('content_settings/', views.content_settings, name='content_settings'),
    path('advanced_settings/', views.advanced_settings, name='advanced_settings'),

    # Add these to accounts/urls.py
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('delete/', views.delete_account, name='delete_account'),



]