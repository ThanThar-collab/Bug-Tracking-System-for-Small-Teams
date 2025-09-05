from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction, connection
from .models import UserProfile, Bug, Project
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
import html
import re
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def userselection_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  
        if user_type in ['developer', 'client', 'admin']:
            request.session['role'] = user_type
            return redirect('signup')
        else:
            messages.error(request, "Please select a valid user type.")
            return redirect('user_register_select')
    return render(request, 'user_register_select.html')

def home_view(request):
    return render(request,"home.html",{})

def about_view(request):
    return render(request,"about.html",{})

def newpage_view(request):
    return render(request,"newpage.html",{})

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
                    role = profile.role  # This will be an integer (1, 2, or 3)
                     # Redirect based on role
                    if role == 1:  # Developer
                        return redirect('developer_dashboard')
                    elif role == 2:  # Tester
                        return redirect('dashboard')
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

def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True  
    messages.success(request, "You have been logged out.")
    return redirect("home")

def dashboard_view(request):
    # bugs = Bug.objects.all()

    # Only show the logged-in user's bugs
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
                reported_by_id=request.user.id,  # use logged-in user
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

    developers = User.objects.filter(userprofile__role=1)  # Only developer users
    context = {
        'developers': developers,
    }
    return render(request, "./dashboard_userinterface/bugreportform.html", context)


# {% if url %}
#     <p>File uploaded: <a href="{{ url }}" target="_blank">Download here</a></p>
# {% endif %}




def developerlogin_view(request):
    return render(request, "developer_login.html", {})

def developersignup_view(request):
    return render(request, "developer_signup.html", {})

def bugdetailmenu_view(request):
    return render(request,"./dashboard_userinterface/bugdetailmenu.html",{})

def userprofile_view(request):
    return render(request,"./dashboard_userinterface/userprofile.html",{})

def developer_dashboard_view(request):
    return render(request,"./developerdashboard_userinterface/developer_dashboard.html",{})

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
        "name": row[2],   # first_name
        "password": row[3],
       
        }
    return render(request,"./dashboard_userinterface/profile.html",context)


def bugdetail_pdf_view(request):
    #create Bytestream buffer
    buf = io.BytesIO()

    #create a canvas
    canva = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    #create a text obj
    textobj = canva.beginText()
    textobj.setTextOrigin(inch, inch)   #text size
    textobj.setFont("Helvetica", 15)

    #add bug data
    # bugs = Bug.objects.filter(reported_by=request.user)
    
    # lines = []

    # for bug in bugs:
    #     lines.append(str(bug.title))
    #     lines.append(str(bug.description))
    #     lines.append(str(bug.reported_by))   # e.g. username
    #     lines.append(str(bug.assigned_to) if bug.assigned_to else "Unassigned")
    #     lines.append(bug.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    #     lines.append(str(bug.desired_date) if bug.desired_date else "")
    #     lines.append(str(bug.severity))
    #     lines.append(" ")  # spacer
    bug = Bug.objects.get(id=bug_id)

    lines = []
    lines.append(f"Title: {bug.title}")
    lines.append(f"Description: {bug.description}")
    lines.append(f"Reporter: {bug.reported_by}")
    lines.append(f"Assignee: {bug.assigned_to if bug.assigned_to else 'Unassigned'}")
    lines.append(f"Created At: {bug.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Desired Date: {bug.desired_date if bug.desired_date else ''}")
    lines.append(f"Severity: {bug.severity}")
    lines.append(" ")  # spacer
        
    #loop
    for line in lines:
        clean_line = html.unescape(str(line))   # decode any &nbsp;, etc.
        textobj.textLine(clean_line)

    #finish up
    canva.drawText(textobj)
    canva.showPage()
    canva.save()
    buf.seek(0)

    safe_bugtitle = re.sub(r'[^\w\-_\. ]', '_', str(bug.title))  # replace invalid chars with _
    return FileResponse(buf, as_attachment=True, filename=f"{safe_bugtitle}.BugDetail.pdf")