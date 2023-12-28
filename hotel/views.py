from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random

def index(request):
    facility = Facility.objects.all().order_by('-id')[:4]
    category = Category.objects.all()
    d = {'category': category,'facility': facility}
    return render(request, 'index.html',d)

def about(request):
    category = Category.objects.all()
    d = {'category': category}
    return render(request, 'about.html',d)

def reg_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    users = User.objects.filter(is_staff=0)
    d = {'users': users}
    return render(request, 'reg_users.html',d)


def read_enquiry(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="yes")
    d = {'contact': contact}
    return render(request, 'read_enquiry.html', d)


def unread_enquiry(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="no")
    d = {'contact': contact}
    return render(request, 'unread_enquiry.html', d)

def view_enquiry(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    d = {'contact': contact}
    return render(request, 'view_enquiry.html', d)



def contact(request):
    error = ""
    category = Category.objects.all()
    if request.method == 'POST':
        n = request.POST['name']
        mn = request.POST['phone']
        e = request.POST['email']
        msg = request.POST['message']
        try:
            Contact.objects.create(name=n,mobilenumber=mn, emailid=e,message=msg,enquirydate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'category': category}
    return render(request, 'contact.html', d)


def signup(request):
    error = ""
    category = Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        e = request.POST['email']
        m = request.POST['mobno']
        p = request.POST['password']
        try:
            User.objects.create_user(username=e, password=p, first_name=f,last_name=m)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category}
    return render(request, 'signup.html',d)



def Login(request):
    error = ""
    category = Category.objects.all()
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error,'category':category}
    return render(request, 'user_login.html',d)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    category = Category.objects.all()
    user=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        f = request.POST['fname']

        m = request.POST['contactnumber']

        user.first_name=f
        user.last_name=m
        try:
            user.save()
            error = "no"
        except:
            error="yes"
    d = {'error':error,'user':user,'category':category}
    return render(request, 'profile.html',d)




def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html',d)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    nbcount = Booking.objects.filter(status="").count()
    abcount = Booking.objects.filter(status="Approved").count()
    cbcount = Booking.objects.filter(status="Cancelled").count()
    ucount = User.objects.filter(is_staff=0).count()
    rcount = Contact.objects.filter(isread="yes").count()
    umcount = Contact.objects.filter(isread="no").count()
    d = {'nbcount': nbcount,'abcount': abcount,'cbcount': cbcount,'ucount': ucount,'rcount': rcount,'umcount': umcount}
    return render(request, 'dashboard.html',d)


def add_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        cn = request.POST['cname']
        cd = request.POST['catdes']
        p = request.POST['price']
        try:
            Category.objects.create(categoryname=cn,description=cd,price=p)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_category.html', d)


def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    d = {'category':category}
    return render(request, 'manage_category.html', d)

def category_details(request,pid):
    category = Category.objects.all()
    category1 = Category.objects.get(id=pid)
    room = Room.objects.filter(roomtype=category1)
    d = {'category':category,'room':room}
    return render(request, 'category_details.html', d)


def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manage_category')



def add_facility(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        ft = request.POST['ftitle']
        im = request.FILES['image']
        fd = request.POST['facdes']
        try:
            Facility.objects.create(facilitytitle=ft,description=fd,image=im)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_facility.html', d)


def manage_facility(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    facility = Facility.objects.all()
    d = {'facility':facility}
    return render(request, 'manage_facility.html', d)


def delete_facility(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    facility = Facility.objects.get(id=pid)
    facility.delete()
    return redirect('manage_facility')



def add_room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    facility = Facility.objects.all()
    error = ""
    if request.method=="POST":
        rt = request.POST['roomtype']
        rn = request.POST['roomname']
        ma = request.POST['maxadult']
        mc = request.POST['maxchild']
        rd = request.POST['roomdes']
        nb = request.POST['nobed']
        im = request.FILES['image']
        rf = ",".join(request.POST.getlist('roomfac'))
        roomtype = Category.objects.get(categoryname=rt)
        try:
            Room.objects.create(roomtype=roomtype,roomname=rn,maxadult=ma,maxchild=mc,roomdescription=rd,noofbed=nb,image=im,roomfacility=rf)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category,'facility':facility}
    return render(request, 'add_room.html', d)


def manage_room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Room.objects.all()
    d = {'room':room}
    return render(request, 'manage_room.html', d)


def delete_room(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Room.objects.get(id=pid)
    room.delete()
    return redirect('manage_room')


def edit_room(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    room = Room.objects.get(id=pid)
    category = Category.objects.all()
    facility = Facility.objects.all()
    error = ""
    if request.method == 'POST':
        rt = request.POST['roomtype']
        rn = request.POST['roomname']
        ma = request.POST['maxadult']
        mc = request.POST['maxchild']
        rd = request.POST['roomdes']
        nb = request.POST['nobed']

        rf = ",".join(request.POST.getlist('roomfac'))
        roomtype = Category.objects.get(categoryname=rt)

        #category1 = Category.objects.get(categoryname=c)
        room.roomtype = roomtype
        room.roomname = rn
        room.maxadult = ma
        room.maxchild = mc
        room.roomdescription = rd
        room.noofbed = nb

        room.roomfacility = rf
        try:
            room.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'room':room,'category':category,'facility':facility}
    return render(request, 'edit_room.html',d)


def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    category = Category.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        cn = request.POST['categoryname']
        des = request.POST['description']
        price = request.POST['price']
        category.categoryname = cn
        category.description = des
        category.price = price
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'category':category}
    return render(request, 'edit_category.html',d)

def edit_facility(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    facility = Facility.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        ft = request.POST['facilitytitle']
        des = request.POST['description']
        facility.facilitytitle = ft
        facility.description = des
        try:
            facility.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'facility':facility}
    return render(request, 'edit_facility.html',d)


def Logout(request):
    logout(request)
    return redirect('index')


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'changepassword.html',d)


def changepassworduser(request):
    if not request.user.is_authenticated:
        return redirect('index')
    category = Category.objects.all()
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error,'category':category}
    return render(request,'changepassworduser.html',d)



def facility(request):
    category = Category.objects.all()
    fac = Facility.objects.all()
    d = {'fac':fac,'category': category}
    return render(request, 'facility.html', d)

def gallery(request):
    category = Category.objects.all()
    room = Room.objects.all()
    d = {'room':room,'category': category}
    return render(request, 'gallery.html', d)


def mybooking(request):
    category = Category.objects.all()
    book = Booking.objects.filter(userid=request.user.id)
    d = {'book':book,'category': category}
    return render(request, 'mybooking.html', d)



def change_image(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Room.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        pic = request.FILES['image']
        room.image = pic
        try:
            room.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'room':room}
    return render(request, 'change_image.html',d)


def change_facilityimage(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    facility = Facility.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        pic = request.FILES['image']
        facility.image = pic
        try:
            facility.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'facility':facility}
    return render(request, 'change_facilityimage.html',d)



def book_room(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')

    category = Category.objects.all()
    error = ""
    bn=""

    if request.method == 'POST':
        bn = str(random.randint(10000000, 99999999))
        id = request.POST['idtype']
        gen = request.POST['gender']
        addr = request.POST['address']
        ci = request.POST['checkindate']
        co = request.POST['checkoutdate']
        room = Room.objects.get(id=pid)
        user = User.objects.get(id=request.user.id)
        try:
            Booking.objects.create(roomid=room,bookingnumber=bn,userid=user,idtype=id,gender=gen,
                                address=addr,checkindate=ci,checkoutdate=co,bookingdate=date.today(),remark="")
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'category':category,'bn':bn}
    return render(request, 'book_room.html',d)


def viewapplicationdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    book = Booking.objects.get(id = pid)
    category = Category.objects.all()
    error = ""
    d = {'error': error,'category':category,'book':book}
    return render(request, 'viewapplicationdetail.html',d)


def invoice(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    book = Booking.objects.get(id = pid)
    category = Category.objects.all()
    totaldays = book.checkoutdate - book.checkindate
    total = totaldays.days * book.roomid.roomtype.price
    error = ""
    d = {'error': error,'category':category,'book':book,'totaldays':totaldays,'total':total}
    return render(request, 'invoice.html',d)


def all_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    book = Booking.objects.all()
    bookcount = Booking.objects.all().count()
    d = {'book':book,'bookcount':bookcount}
    return render(request,'all_booking.html', d)


def newbooking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    book = Booking.objects.filter(status="")
    bookcount = Booking.objects.filter(status="").count()
    d = {'book':book,'bookcount':bookcount}
    return render(request,'newbooking.html', d)

def approved_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    book = Booking.objects.filter(status="Approved")
    bookcount = Booking.objects.filter(status="Approved").count()
    d = {'book':book,'bookcount':bookcount}
    return render(request,'approved_booking.html', d)


def cancelled_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    book = Booking.objects.filter(status="Cancelled")
    bookcount = Booking.objects.filter(status="Cancelled").count()
    d = {'book':book,'bookcount':bookcount}
    return render(request,'cancelled_booking.html', d)



def booking_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    book = Booking.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        rem = request.POST['remark']
        st =  request.POST['status']
        book.remark = rem
        book.status = st
        try:
            book.save()
            error = "no"
        except:
            error = "yes"
    d = {'book':book,'error':error}
    return render(request,'booking_detail.html', d)


def search_enquiry(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    terror = ""
    contact=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            contact = Contact.objects.filter(Q(name=sd)|Q(mobilenumber=sd))
            terror = "found"
        except:
            terror="notfound"
    d = {'contact':contact,'terror':terror,'sd':sd}
    return render(request,'search_enquiry.html',d)



def search_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    terror = ""
    book=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            book = Booking.objects.filter(bookingnumber=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'book':book,'terror':terror,'sd':sd}
    return render(request,'search_booking.html',d)



def enquirybetweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'enquirybetweendate_reportdetails.html')



def enquirybetweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        contact = Contact.objects.filter(Q(enquirydate__gte=fd) & Q(enquirydate__lte=td))
        contactcount = Contact.objects.filter(Q(enquirydate__gte=fd) & Q(enquirydate__lte=td)).count()
        d = {'contact': contact,'fd':fd,'td':td,'contactcount':contactcount}
        return render(request, 'enquirybetweendate_reportdetails.html', d)
    return render(request, 'enquirybetweendate_report.html')



def bookingbetweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'bookingbetweendate_reportdetails.html')



def bookingbetweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        booking = Booking.objects.filter(Q(bookingdate__gte=fd) & Q(bookingdate__lte=td))
        bookingcount = Booking.objects.filter(Q(bookingdate__gte=fd) & Q(bookingdate__lte=td)).count()
        d = {'booking':booking,'fd':fd,'td':td,'bookingcount':bookingcount}
        return render(request, 'bookingbetweendate_reportdetails.html', d)
    return render(request, 'bookingbetweendate_report.html')


