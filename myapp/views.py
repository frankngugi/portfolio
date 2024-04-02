from django.http import Http404, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, login as auth_login
from django.urls import include
from .models import Events, Payment, Member, RegisteredEvent
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserUpdateForm, UserProfileUpdateForm




@login_required(login_url='/accounts/register')
def dashboard(request):
    return render(request,'index')

# Create your views here.
def index(request):
    # View for the home page of the website
    event = Events.objects.all()
    return render(request, 'index.html', {'event': event})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        phonenumber = request.POST['phonenumber']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username already exists.")
            user = User.objects.get(email=email)
            messages.error(request, "Username already exists.")
            return redirect('register') 
        except User.DoesNotExist:
            if len(username) < 5 or len(password) < 8:
                messages.error(request, "Username must be at least 5 characters and Password must be at least 8 characters")
                messages.error(request, "Username and Password must be at least 5 characters long.")
                return redirect('register')
            
            elif password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('register')
                
            else:
                user = User.objects.create_user(username=username, password=password, email=email, phonenumber=phonenumber)
                user.save();
                return redirect('login')
        
    return render(request, 'register.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')

@login_required
def logout(request):
    auth.logout(request);
    return redirect('/');

@login_required 
def profile(request):
    # View to display the registration form
    
    if request.method == 'GET':
        registered_events = RegisteredEvent(request).get_registration_list()
        context = {
            'name' : request.user.getName(),
            'phoneNumber' : request.user.getPhoneNumber(),
            'email' : request.user.getEmail(),
            'userId' : request.user.getUserId(),
        }
        return render(request,'profile.html',context)
      
    elif request.method == 'POST':
        action = request.POST['action']
        
        if action == 'editProfile':
            user_profile = get_object_or_404(Member, user=request.user)  # Retrieve user profile
            user_update_form = UserUpdateForm(request.POST, instance=request.user)
            profile_update_form = UserProfileUpdateForm(request.POST, instance=user_profile)

            if user_update_form.is_valid() and profile_update_form.is_valid():
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, "Changes saved successfully!")
                return redirect('profile')  # Redirect to profile page after saving
            else:
                # Handle form validation errors
                context = {'user_update_form': user_update_form}
                
                for field in user_update_form.errors:
                    messages.error(request, "%s %s" % (field.capitalize(), user_update_form.errors[field][0]))
                    context[field] = user_update_form.errors[field]
                return render(request, 'profile.html', context)

        elif action == 'addEvent':
            event_id = int(request.POST['event'])
            try:
                event = Events.objects.get(id=event_id)  # Retrieve the event object
                RegisteredEvent.objects.create(user=request.user, event=event)  # Create a new registration
            except object.DoesNotExist:
    # Handle the case where the event doesn't exist
                raise Http404("Event not found")
            events = RegisteredEvent.objects.filter(user=request.user)
            context = {'events' : events}
            return JsonResponse(context)
            
        elif action == 'removeEvent':
            event_id = int(request.POST['event'])
            try:
                registration = RegisteredEvent.objects.get(user=request.user, event_id=event_id)
                registration.delete()  # Delete the registration
            except object.DoesNotExist:
                # Handle the case where the registration doesn't exist
                raise Http404("Event not found")

            events = RegisteredEvent.objects.filter(user=request.user)
            context = {'events' : events}
            return JsonResponse(context)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])
              
        
    else:
        return HttpResponseNotAllowed(['GET','POST'])


@login_required
def account(request):
    """View for displaying the current user's profile page."""

    user = request.user
    profile = Member.objects.get(user=user)  # Assuming a one-to-one relationship with UserProfile

    if request.method == 'GET':
        # Create an instance of the UserUpdateForm with user's data
        form = UserUpdateForm(instance=profile)
        context = {'form': form}
        return render(request, 'account/account.html', context)

    elif request.method == 'POST':
        # Update the form with submitted data
        form = UserUpdateForm(request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            # Save the updated profile data to the database
            form.save()
            messages.success(request, "Your profile has been successfully saved!")
            return redirect('account')  # Redirect to the same page after saving
        else:
            # Handle form validation errors
            context = {'form': form}
            return render(request, 'account/account.html', context)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


# @(['GET', 'POST'])  # Allow both GET and POST requests
def change_password(request):
    """View for changing the password of the current logged in user."""
    user = request.user
    form = PasswordChangeForm(user=user)  # Create form based on user

    if request.method == 'GET':
        return render(request, "account/change_password.html", {"form": form})

    elif request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)  # Bind submitted data
        if form.is_valid():
            form.save()  # Save the updated password
            logout(request)  # Log the user out for security
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('login')  # Redirect to login page after success
        else:
            return render(request, "change_password.html", {"form": form})



    return render(request, 'register.html' )



def gallery(request):
    return render(request, 'gallery.html' )

def chats(request):
    return render(request, 'chats.html' )

def videos(request):
    return render(request, 'videos.html' )
