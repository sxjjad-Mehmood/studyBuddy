from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django .contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Topic,Room,Message
from .forms import RoomForm,UserForm

# Create your views here.
def loginpage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User don't Exits")
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user) # this login build method used make session start addin the datbase
            return redirect("home")
        else:
            messages.error(request,"Username and Password is incorrect")
    context={'page': page}
    return render(request,'login-register.html',context)

def logoutuser(request):
    logout(request)
    return redirect('home') 
def loginregister(request):
    form =UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occur during the registration")
    return render(request,"login-register.html",{'form':form})



def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q) 
        )
    topics=Topic.objects.all()[0:5]
    rooms_count=rooms.count()
    roommessages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'roommessages':roommessages}
    return render(request,'home.html',context)
def room(request,pk):
    rooms=Room.objects.get(id=pk)
    room_message=rooms.message_set.all().order_by('-created') #for many to one releationship
    participants=rooms.participants.all()#for many to many relationship
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect("room",pk=rooms.id)

    context={"rooms":rooms,"participants":participants,"room_message":room_message}
    return render(request,'room.html',context)
def user_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    roommesages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'roommessages':roommesages,'topics':topics}
    return render(request,'profile.html',context)

@login_required(login_url='login')
def room_created(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
       topic_name = request.POST.get('topic')
       topic, created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host= request.user,
           topic=topic,
           name=request.POST.get('name'), # automatically get the form from because django use model which automatically creates form basis on model
           description=request.POST.get('description'),
       )
       return redirect('home')
    context={'form':form, 'topics':topics}
    return render(request,'room_form.html',context)
@login_required(login_url='login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    topics=Topic.objects.all()
    form=RoomForm(instance=room)
    if request.user!=room.host:
        return HttpResponse(" you are not allowed here")
    if request.method=='POST':
          topic_name = request.POST.get('topic')
          topic, created = Topic.objects.get_or_create(name=topic_name)
          room.name=request.POST.get('name')
          room.topic=topic
          room.description=request.POST.get('description')
          room.save()
          return redirect('home')
    

    context={'form':form ,'topics':topics,'room':room}
    return render(request, 'room_form.html', context)
@login_required(login_url='login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse(" you are not allowed here")
    if request.method=='POST':
        room.delete()
        return redirect("home")
    return render(request,'delete.html',{'obj':room})
@login_required(login_url='login')
def deletemessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("You are not allowed here")
    if request.method=="POST":
        message.delete()
        return redirect("home")
    return render(request,"delete.html",{'obj':message})
@login_required(login_url='login')
def updateuser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method == 'POST':
       form = UserForm(request.POST,instance=user)
       if form.is_valid():
          form.save()
          return redirect('user_profile',pk=user.id)
    return render(request,"update-user.html",{'form': form})
def topicpage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topic=Topic.objects.filter(name__icontains=q)
    return render (request,"topics.html",{'topics':topic})
def activitypage(request):
    room_messages=Message.objects.all()
    return render(request,"activity.html", {'roommessages':room_messages})


