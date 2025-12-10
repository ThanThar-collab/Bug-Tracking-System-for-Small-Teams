from django.urls import path
from . import views

urlpatterns = [
    #home website
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
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('bugreportform/', views.bugreportform_view, name='bugreportform'),
    path('bugdetailmenu/', views.bugdetailmenu_view, name='bugdetailmenu'),
    path('userprofile/', views.userprofile_view, name='userprofile'),
    path('profile/', views.profile_view, name='profile'),
    path('bugdetail_pdf/', views.bugdetail_pdf_view, name='bugdetail_pdf'),

    #developer dashboard
    path('developer_kanban_dashboard/', views.kanbanDashboard_view, name='developer_kanban_dashboard'),
    path('developer_dashboard/', views.developer_dashboard_view, name='developer_dashboard'),
    path('developer_profile/', views.developer_profile_view, name='developer_profile'),
    path('api/fetch-bugs/', views.fetch_bugs, name='fetch_bugs'),

    #admin dashboard
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('manage_users/', views.manage_user_view, name='manage_users'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('validate_bug/<int:bug_id>/', views.validate_bug, name='validate_bug'),
    path('bug_list/', views.bug_list_view, name='bug_list'),
    path('manage_bugs/', views.manage_bugs_view, name='manage_bugs'),
    # Note: bug_edit_view is not in views.py, so it's commented out here. 
    # You will need to implement or remove the link from bugManagement.html if not needed.
    # path('bug/<int:bug_id>/edit/', views.bug_edit_view, name='bug_edit'),
    path('bug/<int:bug_id>/delete/', views.delete_bug_view, name='bug_delete'), # Uses existing delete_bug_view
]