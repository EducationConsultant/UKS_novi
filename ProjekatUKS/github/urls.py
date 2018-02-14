from django.urls import path

from . import views

app_name = 'github'
urlpatterns = [
    path('', views.switch_home, name='home'),
    path('registration', views.switch_registration, name='registration'),
    path('save_user', views.save_user, name='save_user'),
    path('activate_user/<username>', views.activate_user, name='activate_user'),

    path('login', views.switch_login, name='login'),
    path('login_user', views.login_user, name='login_user'),

    path('forgot_password', views.switch_forgot_password, name='forgot_password'),
    path('reset_password/', views.send_email_reset_password, name='reset_password'),
    path('password_reset/<username>', views.switch_forgot_password_reset, name='password_reset'),
    path('insert_reset_password', views.reset_password, name='insert_reset_password'),

    path('logout', views.logout, name='logout'),

    path('about_user',views.about_user, name='about_user'),

    path('switch_change_username',views.switch_change_username, name='switch_change_username'),
    path('change_username',views.change_username, name='change_username'),

    path('switch_change_password',views.switch_change_password, name='switch_change_password'),
    path('change_password',views.change_password, name='change_password'),

    path('switch_delete_account',views.switch_delete_account, name='switch_delete_account'),
    path('delete_account',views.delete_account, name='delete_account'),

    path('organization', views.organization, name='organization'),
    path('saveOrganization', views.saveOrganization, name='saveOrganization'),
    path('saveOrganizationDetails', views.saveOrganizationDetails, name='saveOrganizationDetails'),


    path('switch_all_issues', views.switch_issue_show_all, name='switch_all_issues'),
    path('issue_show_all_open', views.issue_show_all_open, name='issue_show_all_open'),
    path('issue_show_all_closed', views.issue_show_all_closed, name='issue_show_all_closed'),

    path('switch_issue_new', views.switch_issue_new, name='switch_issue_new'),
    path('issue_new', views.issue_new, name='issue_new'),
    path('switch_issue_view_one/<id>', views.switch_issue_view_one, name='switch_issue_view_one'),
    path('issue_edit_title/<id>', views.issue_edit_title, name='issue_edit_title'),
    path('issue_close/<id>', views.issue_close, name='issue_close'),
    path('issue_reopen/<id>', views.issue_reopen, name='issue_reopen'),

    path('saveOrganizationMembers/<str:name>', views.saveOrganizationMembers, name='saveOrganizationMembers'),
    path('repository/<str:p>', views.repository, name='repository'),
    path('saveRepository/<str:p>', views.saveRepository, name='saveRepository'),
    path('saveRepositoryMembers/<str:name>', views.saveRepositoryMembers, name='saveRepositoryMembers'),
    path('repositoriesShow', views.repositoriesShow, name='repositoriesShow'),
    path('organizationsShow', views.organizationsShow, name='organizationsShow'),
    path('organizationInfo/<str:name>', views.organizationInfo, name='organizationInfo'),
    path('addNewMemberOrganization/<str:name>', views.addNewMemberOrganization, name='addNewMemberOrganization'),
    path('repositoryInfo/<str:name>', views.repositoryInfo, name='repositoryInfo'),
    path('addNewMemberRepository/<str:name>', views.addNewMemberRepository, name='addNewMemberRepository'),


]