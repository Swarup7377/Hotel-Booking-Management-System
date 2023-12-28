"""hotelbooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('about',about, name='about'),
    path('contact',contact, name='contact'),
    path('facility',facility, name='facility'),
    path('gallery',gallery, name='gallery'),
    path('signup',signup, name='signup'),
    path('user_login',Login, name='user_login'),
    path('profile',profile, name='profile'),
    path('category_details/<int:pid>',category_details, name='category_details'),
    path('admin_login', admin_login, name='admin_login'),
    path('dashboard',dashboard, name='dashboard'),
    path('add_category',add_category, name='add_category'),
    path('manage_category',manage_category, name='manage_category'),
    path('delete_category/<int:pid>', delete_category,name='delete_category'),
    path('add_facility',add_facility, name='add_facility'),
    path('manage_facility',manage_facility, name='manage_facility'),
    path('delete_facility/<int:pid>', delete_facility,name='delete_facility'),
    path('delete_room/<int:pid>', delete_room,name='delete_room'),
    path('add_room',add_room, name='add_room'),
    path('manage_room',manage_room, name='manage_room'),
    path('edit_room/<int:pid>',edit_room,name='edit_room'),
    path('edit_category/<int:pid>',edit_category,name='edit_category'),
    path('edit_facility/<int:pid>',edit_facility,name='edit_facility'),
    path('changepassword',changepassword, name='changepassword'),
    path('changepassworduser',changepassworduser, name='changepassworduser'),
    path('logout',Logout, name='logout'),
    path('reg_users',reg_users, name='reg_users'),
    path('read_enquiry',read_enquiry, name='read_enquiry'),
    path('unread_enquiry',unread_enquiry, name='unread_enquiry'),
    path('view_enquiry/<int:pid>',view_enquiry, name='view_enquiry'),
    path('change_image/<int:pid>',change_image, name='change_image'),
    path('change_facilityimage/<int:pid>',change_facilityimage, name='change_facilityimage'),
    path('book_room/<int:pid>', book_room, name='book_room'),
    path('viewapplicationdetail/<int:pid>',viewapplicationdetail, name='viewapplicationdetail'),
    path('invoice/<int:pid>',invoice, name='invoice'),
    path('mybooking',mybooking, name='mybooking'),
    path('all_booking',all_booking, name='all_booking'),
    path('newbooking',newbooking, name='newbooking'),
    path('approved_booking',approved_booking, name='approved_booking'),
    path('cancelled_booking',cancelled_booking, name='cancelled_booking'),
    path('booking_detail/<int:pid>',booking_detail, name='booking_detail'),
    path('search_enquiry',search_enquiry, name='search_enquiry'),
    path('search_booking',search_booking, name='search_booking'),
    path('bookingbetweendate_reportdetails',bookingbetweendate_reportdetails, name='bookingbetweendate_reportdetails'),
    path('bookingbetweendate_report',bookingbetweendate_report, name='bookingbetweendate_report'),
    path('enquirybetweendate_reportdetails',enquirybetweendate_reportdetails,name='enquirybetweendate_reportdetails'),
    path('enquirybetweendate_report',enquirybetweendate_report, name='enquirybetweendate_report'),
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
