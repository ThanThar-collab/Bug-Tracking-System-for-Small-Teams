from django.urls import path
from . import views

urlpatterns = [
    #home websit
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('newpage/', views.newpage_view, name='newpage'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('user_register_select/', views.userselection_view, name='user_register_select'),
    path('developer_login/', views.developerlogin_view, name='developer_login'),
    path('developer_signup/', views.developersignup_view, name='developer_signup'),

    #client dashboard
    path('dashboard_userinterface/dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard_userinterface/bugreportform/', views.bugreportform_view, name='bugreportform'),
    path('dashboard_userinterface/bugdetailmenu/', views.bugdetailmenu_view, name='bugdetailmenu'),
    path('dashboard_userinterface/userprofile/', views.userprofile_view, name='userprofile'),
    path('dashboard_userinterface/profile/', views.profile_view, name='profile'),
    path('dashboard_userinterface/dashboard/bugdetail_pdf', views.bugdetail_pdf_view, name='bugdetail_pdf'),


    #developer dashboard
    path('developerdashboard_userinterface/developer_dashboard/', views.developer_dashboard_view, name='developer_dashboard'),
] 