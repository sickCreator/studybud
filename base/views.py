from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.http import HttpResponse
# Create your views here.
# request object tells what kind of data being sent to server
# or what knid of request is being sent to the backend/
# the room list is now commented as we will work on databases.
# rooms= [
#     {
#         'id':1,
#         'name': '''let's Learn python'''
#     },
#     {
#         'id':2,
#         'name': '''let's Learn java'''
#     },
#     {
#         'id':3,
#         'name': '''let's Learn c++'''
#     },
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # checking if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            # if user exists chhecking if credentials are correct
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is incorrect')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # to clean data before saving it
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form, 'page': page})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # .all() will give all the objects on the database
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    # Topic.objects.all()[0:5] will give fist 0 to 5 topics of all topics.
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    # room_messages =Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, "topics": topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # room =none;
    # for i in rooms:
    #     # simply a method of extracting values of a dictionart can also
    #     # be done as i.id.
    #     if i['id'] == int(pk):
    # room = i
    # (set of msgs related to specific room)message_set.all() quering child objects of a specific room
    # so the most recently created msg will be first
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    # getting all the topics and passing to template
    topics = Topic.objects.all()
    if request.method == 'POST':
        # get new topic value created by user for a room if not present
        topic_name = request.POST.get('topic')
        # get or Create will return back a object or will return a object and create it and rdeturn it
        # if we pass in a topic name for name value, get or create will get value of (topic) opject and return it insidde in
        # topic object
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     # an instance of room is created instead of just subnitting
        #     room = form.save(commit=False)
        #     # host will be created based on whoever is the user.
        #     room.host = request.user
        #     room.save()
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    # The form will be prefilled with the room value
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    form = RoomForm(instance=room)
    if request.method == 'POST':
       # get new topic value created by user for a room if not present
        topic_name = request.POST.get('topic')
        # get or Create will return back a object or will return a object and create it and rdeturn it
        # if we pass in a topic name for name value, get or create will get value of (topic) opject and return it insidde in
        # topic object
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.Post.get('name')
        room.topic = topic
        room.description = request.Post.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    # here user in message.user is the owner of the message
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # until filter is added this will finction as .all()
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activities(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
