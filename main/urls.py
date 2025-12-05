from django.urls import path
from . import views

urlpatterns=[
    path("login/",views.loginpage,name='login'),
    path("logout/",views.logoutuser,name='logout'),
    path("register/",views.loginregister,name='register'),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('room_created/',views.room_created,name='room-created'),
    path('room_updated/<str:pk>/',views.updateroom,name='update-room'),
    path('room_delete/<str:pk>/',views.deleteroom,name='delete-room'),
    path('message_delete/<str:pk>/',views.deletemessage,name='delete_message'),
    path("profile/<str:pk>/",views.user_profile,name='user_profile'),
    path("update-user/",views.updateuser,name='update-user'),
    path("topic/",views.topicpage,name = 'topic'),
    path("activity/",views.activitypage,name = 'activity')
]
