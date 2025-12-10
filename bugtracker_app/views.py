from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from .models import UserProfile, Bug
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
import io
import html
import re
import logging
logger = logging.getLogger(__name__)


def userselection_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  
        if user_type in ['developer', 'client']:
            request.session['role'] = user_type
            return redirect('signup')
        else:
            messages.error(request, "Please select a valid user type.")
            return redirect('user_register_select')
    return render(request, 'user_register_select.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_authenticated:
                messages.success(request, ("You Have Been Logged In!"))
             # Get user profile
                try:
                    profile = UserProfile.objects.get(user=user)
                    role = profile.role
                     # Redirect based on role
                    if role == 1:  # Developer
                        return redirect('developer_dashboard')
                    elif role == 2:  # Tester
                        return redirect('dashboard')
                    elif role == 3:
                        return redirect('admin_dashboard')
                    else:
                        return redirect('home')
                except UserProfile.DoesNotExist:
                    messages.error(request, "Profile not found.")
                    return redirect('login')    
    
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "login.html", {})

def signup_view(request):
    role_map = {'developer':1, 'client':2, 'admin':3} 
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        role_str = request.session.get('role')
        role = role_map.get(role_str)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )
        user.save()

        profile = UserProfile(user=user, role=role)
        profile.save()
        del request.session['role']

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user.userprofile, 'role', None) == 3)

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    last_week = timezone.now() - timedelta(days=7)

    total_clients = User.objects.filter(userprofile__role=2).count()
    total_developers = User.objects.filter(userprofile__role=1).count()
    total_users = User.objects.count()

    total_bugs = Bug.objects.count()
    pending_bugs = Bug.objects.filter(validity='Pending').count()
    open_bugs = Bug.objects.filter(status__in=['Open', 'New', 'In Progress']).count()
    resolved_this_week = Bug.objects.filter(
        status__in=['Resolved', 'Closed'],
        updated_at__gte=last_week
    ).count()

    recent_bugs = Bug.objects.all().order_by('-created_at')[:10]

    context = {
        'total_bugs': total_bugs,
        'total_clients': total_clients,
        'total_developers': total_developers,
        'total_users': total_users,
        'pending_bugs': pending_bugs,
        'open_bugs': open_bugs,
        'resolved_this_week': resolved_this_week,
        'recent_bugs': recent_bugs,
    }
    # FIXED: Added app prefix
    return render(request, "admindashboard_userinterface/admin_dashboard.html", context)

@user_passes_test(is_admin)
def bug_list_view(request):
    bugs = Bug.objects.all().order_by('-created_at')
    # FIXED: Added app prefix
    return render(request, 'admindashboard_userinterface/bug_list.html', {"bugs": bugs})

@user_passes_test(is_admin)
def validate_bug(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment')
        severity = request.POST.get('severity')

        if action in ['valid', 'invalid', 'duplicate']:
            bug.validity = action.capitalize()
            bug.status = bug.validity

        else :
            messages.error(request, "Invalid action selected")
            return redirect('bug_list')

        bug.admin_comments = comment
        if severity:
            bug.severity = severity
        bug.save()

        return redirect('bug_list')
    
    return redirect('bug_list')

@user_passes_test(is_admin)
def manage_user_view(request):
    users = User.objects.exclude(is_superuser=True)
    # FIXED: Added app prefix
    return render(request, 'admindashboard_userinterface/userManagement.html', {'users': users})


@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('manage_users')

@user_passes_test(is_admin)
@login_required
def manage_bugs_view(request):
    # Fetch all bugs and order them
    all_bugs = Bug.objects.all().order_by('-created_at')
    
    # Calculate stats for the cards
    total_bugs = all_bugs.count()
    open_bugs = all_bugs.filter(status='Open').count()
    in_progress_bugs = all_bugs.filter(status='In Progress').count()
    
    # Calculate bugs closed this week (example logic)
    one_week_ago = timezone.now() - timedelta(days=7)
    closed_this_week = all_bugs.filter(status='Closed', created_at__gte=one_week_ago).count()

    context = {
        'bugs': all_bugs,
        'total_bugs': total_bugs,
        'open_bugs': open_bugs,
        'in_progress_bugs': in_progress_bugs,
        'closed_this_week': closed_this_week,
    }
    # FIXED: Added app prefix
    return render(request, 'admindashboard_userinterface/bugManagement.html', context)

@user_passes_test(is_admin)
def delete_bug_view(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)
    title =  bug.title
    bug.delete()
    messages.success(request, f"Bug '{title}' deleted successfully.")
    return redirect('manage_bugs')

# Create your views here.


def home_view(request):
    return render(request,"home.html",{})

def about_view(request):
    return render(request,"about.html",{})

def newpage_view(request):
    return render(request,"newpage.html",{})


def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True  
    messages.success(request, "You have been logged out.")
    return redirect("home")

def dashboard_view(request):
    bugs = Bug.objects.filter(reported_by=request.user).order_by('-created_at')

    context = {
        "bugs": bugs
    }

    return render(request,"./dashboard_userinterface/dashboard.html", context)

def bugreportform_view(request):
    if request.method == "POST":
        title = request.POST.get("bug_title")
        description = request.POST.get("bug_description")
        attachment = request.FILES.get("uploaded_file")
        assigned_to_id = request.POST.get("assign_to")
        desired_date = request.POST.get("desired_date")
        severity = request.POST.get("severity")
        status = request.POST.get("status", 'Open') 
          
        assigned_to = None
        if assigned_to_id:
            try:
                assigned_to = User.objects.get(id=assigned_to_id)
            except User.DoesNotExist:
                logger.error(f"User with ID {assigned_to_id} not found")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": "Assigned user not found"})
        
        # Create Bug
        try:
            bug = Bug.objects.create(
                title=title,
                description=description,
                attachment=attachment,
                desired_date=desired_date,
                assigned_to_id=assigned_to.id if assigned_to else None,
                reported_by_id=request.user.id,
                severity=severity,
                status=status,
            )
            bug.save()
            logger.info(f"Bug created successfully: {bug}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "bug_id": bug.id})

            return redirect("bugreportform")  

        except Exception as e:
            logger.error(f"Error creating bug: {str(e)}")

            messages.error(request, f"Error creating bug: {str(e)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": str(e)})

    developers = User.objects.filter(userprofile__role=1)
    context = {
        'developers': developers,
    }
    return render(request, "./dashboard_userinterface/bugreportform.html", context)


def developerlogin_view(request):
    return render(request, "developer_login.html", {})

def developersignup_view(request):
    return render(request, "developer_signup.html", {}) 

def bugdetailmenu_view(request):
    return render(request,"./dashboard_userinterface/bugdetailmenu.html",{})

def userprofile_view(request):
    return render(request,"./dashboard_userinterface/userprofile.html",{})

def kanbanDashboard_view(request):
    return render(request,"./developerdashboard_userinterface/developer_kanban_dashboard.html",{})

def developer_dashboard_view(request):
    bugs = Bug.objects.filter(assigned_to=request.user).order_by('-created_at')
    context = {"bugs": bugs}
    return render(request,"./developerdashboard_userinterface/developer_dashboard.html",context)

@login_required
def profile_view(request):
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT u.username, u.email, u.first_name, u.password
        FROM auth_user as u
        WHERE id = %s
        """, [user_id])
        row = cursor.fetchone()

        context = {}
    if row:
        context = {
        "username": row[0],
        "email": row[1],
        "name": row[2],
        "password": row[3],
       
        }
    return render(request,"./dashboard_userinterface/profile.html",context)


def bugdetail_pdf_view(request):
    buf = io.BytesIO()
    canva = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = canva.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 15)
    bugs = Bug.objects.filter(reported_by=request.user)
    
    lines = []

    for bug in bugs:
        lines.append(str(bug.title))
        lines.append(str(bug.description))
        lines.append(str(bug.reported_by))
        lines.append(str(bug.assigned_to) if bug.assigned_to else "Unassigned")
        lines.append(bug.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        lines.append(str(bug.desired_date) if bug.desired_date else "")
        lines.append(str(bug.severity))
        lines.append(" ")
        
    for line in lines:
        clean_line = html.unescape(str(line))
        textobj.textLine(clean_line)

    canva.drawText(textobj)
    canva.showPage()
    canva.save()
    buf.seek(0)

    filename = "BugDetails.pdf"
    if bugs.exists():
        filename = f"{re.sub(r'[^\w\-_\. ]', '_', bugs.first().title)}_Details.pdf"
    return FileResponse(buf, as_attachment=True, filename=filename)


def developer_profile_view(request):
    return render(request, "./developerdashboard_userinterface/developer_profile.html", {})

def fetch_bugs(request):
    bugs = Bug.objects.filter(assigned_to=request.user).values(
        "id", "title", "description", "status", "severity", "assigned_to__username", "reported_by__username"
    )
    return JsonResponse(list(bugs), safe=False)