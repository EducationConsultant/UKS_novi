from django.urls import path

from . import views

app_name = 'github'
urlpatterns = [
    path('', views.home, name='home'),
    path('registration', views.registration, name='registration'),
    path('saveUser', views.saveUser, name='saveUser'),
    path('activate_user/<username>', views.activate_user, name='activate_user'),
    path('login', views.login, name='login'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout, name='logout'),
    path('about_user',views.about_user, name='about_user'),
    path('change_username',views.change_username, name='change_username'),
    path('change_password',views.change_password, name='change_password'),
    path('delete_account',views.delete_account, name='delete_account'),
    path('organization', views.organization, name='organization'),
    path('saveOrganization', views.saveOrganization, name='saveOrganization'),
    path('saveOrganizationDetails', views.saveOrganizationDetails, name='saveOrganizationDetails'),
    path('saveOrganizationMembers', views.saveOrganizationMembers, name='saveOrganizationMembers'),
]