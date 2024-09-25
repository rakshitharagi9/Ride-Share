from django.contrib import admin
from django.urls import path, include
from authentication.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from chat.views import *

urlpatterns = [
    path('', home, name="recipes"),  # Home page
    path("admin/", admin.site.urls),  # Admin interface
    path('login/', login_page, name='login_page'),  # Login page
    #path('logout/', logout, name='logout'),
    path('register/', register_page, name='register'),  # Registration page
    path('mainpage/', main_page, name='mainpage'),  # Main page
    path("publisher/", publisher_page, name="publisher"),
    path("publisherdatabase", publisher_database, name="publisherdatabase"),
    path("searchforpublisher", search_for_publisher, name="searchforpublisher"),
    path("request/", request_page, name="request"),
    path("no_rides/", no_rides, name="no_rides"),
    path("chat/", chat_page, name="chat"),
    path("sendingrequest", sendingrequest_page, name="sendingrequest"),
    path("rejectrequest", rejectrequest_page, name="rejectrequest"),
    path("acceptrequest", acceptrequest_page, name="acceptrequest"),
    path("your_rides/", your_rides, name="your_rides"),
    path("profile/", profile_page, name="profile"),
    path("edit/", edit_page, name="edit"),
    path("edited/", edited_page, name="edited"),
    path('delete_published_ride/', delete_published_ride, name='delete_published_ride'),
    path('delete_passenger_ride/', delete_passenger_ride, name='delete_passenger_ride'),
    path('finish_ride/', finish_ride, name='finish_ride'),
    path('submit_rating/', submit_rating, name='submit_rating'),
    path('thank_you/', thank_you, name='thank_you'),

    path('chat_home/', chathome, name='chat_home'),
    path('submit_rating/', submit_rating, name='submit_rating'),
    path('chat_home/checkview', checkview, name='checkview'),
    path('send', send, name='send'),
    path('getMessages/<str:room>/', getMessages, name='getMessages'),
    path('<str:room>/', room, name='room'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
