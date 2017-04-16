from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Property, Visitor, Owner, Rented, Review, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
import urllib.request
import json 

##########################################################

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def login_user(request):
    error = None
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            current_user = request.user
            if(current_user.is_owner):
                return redirect("ownerdashboard")
            else:
                return redirect("dashboard")
        else:
            error = "Invalid credentials. Try again."
    return render(request, "login.html", {'error':error})

##########################################################
@login_required
def dashboard(request):

    if(request.method == "POST"):
        cursor = connection.cursor()
        sortBy = 'avg_rating'
        current_user = request.user
        visitor = Visitor.obects.get(user = current_user)
        preferred_location = visitor.pref_location
        if request.POST['sortBy'] == '1':
            sortBy = 'avg_rating'
        # elif request.POST['sortBy'] == '2':
        #     cursor.execute('SELECT id, location from property');
        #     prop_list1 = dictfetchall(cursor)
        #     prop_list = []
        #     url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
        #     for i in prop_list1:
        #         prop_id = int(i['id'])
        #         url += i['location']
        #         url += "&destinations="
        #         url += preferred_location
        #         url += "&key=AIzaSyC6h2gHIWNCKwSNJzBNrYoimC068Ma34KA"
        #         req = urllib.request.Request(url)
        #         response = urllib.request.urlopen(req)
        #         json_data = response.read().decode('ascii')
                # res = json.loads(json_data)
        #         for index, i in enumerate(res['rows']):
        #             for j in i['elements']:
        #                 if j['distance']['value'] > 1000:
        #                     cursor.execute('SELECT * FROM property WHERE id = %d', [prop_id]);
        #                     answer = dictfetchall(cursor)
                            
        elif request.POST['sortBy'] == '3':
            sortBy = 'price'



        if request.POST['query'] == '1':
            x = float(request.POST['val'])
            cursor.execute('SELECT * FROM property WHERE avg_rating >= %f ORDER BY %s', [x, sortBy]);
            prop_list = dictfetchall(cursor)
        elif request.POST['query'] == '2':
            x = int(request.POST['val'])
            cursor.execute('SELECT prop_id, location, num_views, description, price, avg_rating FROM property NATURAL JOIN (SELECT prop_id, COUNT(*) as c FROM review WHERE rating = 5 GROUP BY prop_id) WHERE c >= %d ORDER BY %s', [x, sortBy]);
            prop_list = dictfetchall(cursor)
        elif request.POST['query'] == '3':
            x = int(request.POST['val'])
            cursor.execute('SELECT id, location FROM property')
            prop_list = dictfetchall(cursor)
        elif request.POST['query'] == '4':
            x = int(request.POST['val'])
            cursor.execute('SELECT * FROM property WHERE price <= %f ORDER BY %s' [x, sortBy])
            prop_list = dictfetchall(cursor)
        # sort_by = request.POST['sortBy']
        # more_than_rating = request.POST['rating']
        # min_x_5_rating = request.POST['minRating']
        # distance_
        # freq_occupied = request.POST['freqOccupied']
        # distance = request.POST['distance']

        #queries implement  
    ##########################################
        # prop_list = Property.objects.all()
        paginator = Paginator(prop_list, 10)
        page = request.GET.get('page')
        try:
            property_disp = paginator.page(page)
        except PageNotAnInteger:
            property_disp = paginator.page(1)
        except EmptyPage:
            property_disp = paginator.page(paginator.num_pages)
        
    return render(request, "visitor_dashboard.html", {})

##########################################################
@login_required
def owner_dashboard(request):
    # if(request.method == POST):
    #   if (request.POST["alphabetical_order"]):
    #       pass    #
    #   if(request.POST['rent_pending']):
    #       pass#
    current_user = request.user
    current_owner = Owner.objects.get(user = current_user)

    return render(request, "owner_dashboard.html",{})

##########################################################

def register(request):
    error = None
    if (request.method =="POST"):
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        existing = User.objects.filter(username__iexact=username)
        if existing.exists():
            error = "This username already exists. Kindly provide another username."
        
        new_user = User.objects.create_user(username = username, password = password, is_owner = True)
        new_user.save()
        new_owner = Owner.objects.create(user = new_user, owner_name = name, num_properties = 0)
        print(new_user)
        # new_owner.user = new_user
        new_owner.save()
        return redirect('login')
    return render(request, "register.html",{'error':error})


##########################################################
@login_required
def add_property(request):
    # if request.method == "POST":
    #   description = request.POST['description']
    #   price = request.POST['price']
    #   location = request.POST['location']
    #   new_prop = Property.objects.create(description=description,price=price,location=location)
    #   new_prop.save()
    #   return redirect('addProperty')
    return render(request, "addProperty.html",{})

##########################################################

def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request,"home.html",{})