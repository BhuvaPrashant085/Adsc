from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Issue
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IssueForm




@login_required(login_url='login')
def home(request):
    issues = Issue.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'issues': issues})


@login_required(login_url='login')
def dashboard(request):
    issues = Issue.objects.all().order_by('-created_at')

    # Dashboard summary data
    total_issues = Issue.objects.count()
    open_issues = Issue.objects.filter(status='Open').count()
    in_progress_issues = Issue.objects.filter(status='In Progress').count()
    closed_issues = Issue.objects.filter(status='Closed').count()

    # Filters
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if status_filter and status_filter != 'All':
        issues = issues.filter(status=status_filter)

    if priority_filter and priority_filter != 'All':
        issues = issues.filter(priority=priority_filter)

    context = {
        'issues': issues,
        'total_issues': total_issues,
        'open_issues': open_issues,
        'in_progress_issues': in_progress_issues,
        'closed_issues': closed_issues,
    }

    return render(request, 'dashboard.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or user does not exist')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists, please login')
            return redirect('login')

        User.objects.create_user(username=username, password=password1)
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, 'signup.html')



def user_logout(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IssueForm()

    return render(request, 'issues/create.html', {'form': form})


