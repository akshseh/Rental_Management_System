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
    error = None  
    cursor = connection.cursor()
    current_user = request.user

    curr_visitor = Visitor.objects.get(user = current_user)

    # to get the current visitor
    #cursor.execute("""SELECT * 
    #    FROM rental_system_visitor
    #    WHERE user_id = %s""", [current_user.id]);
    #curr_visitor = dictfetchall(cursor)[0]
    #print(curr_visitor)

    cursor.execute("""
        SELECT T.id, T.description, T.price, T.location, T.num_views
        FROM rental_system_property as T 
        WHERE id NOT IN 
            (SELECT prop_id_id 
             FROM   rental_system_rented)""");#Now it gets linked to the Google API and then gets sorted on the basis of distance
    prop_list = dictfetchall(cursor)
    
    myprop = Rented.objects.filter(visitor_id = curr_visitor)
    
    # cursor.execute("""SELECT *
    #     FROM rental_system_rented
    #     WHERE visitor_id_id = %s""", [curr_visitor.id]);

    paginator = Paginator(prop_list, 2)
    page = request.GET.get('page')
    try:
        property_disp = paginator.page(page)
    except PageNotAnInteger:
        property_disp = paginator.page(1)
    except EmptyPage:
        property_disp = paginator.page(paginator.num_pages)
    
    cursor.execute("""
        SELECT T.id, T.description, T.price, T.location, T.num_views
        FROM rental_system_property as T 
        WHERE id IN 
            (SELECT prop_id_id 
             FROM   rental_system_rented
             WHERE  visitor_id_id = %s)""",[curr_visitor.id]);
    rent_list = dictfetchall(cursor)
    
    # paginator1 = Paginator(rent_list, 2)
    # page2 = request.GET.get('page')
    # try:
    #     rent_disp = paginator1.page(page)
    # except PageNotAnInteger:
    #     rent_disp = paginator1.page(1)
    # except EmptyPage:
    #     rent_disp = paginator1.page(paginator.num_pages)


    if(request.method == "POST"):
        # if (request.POST)

        # if request.POST['val'] == "":
        #     error = "please enter an integer value in input field."
        # else:
        #     sortBy = 'avg_rating'
        #     print(request.POST)
        #     preferred_location = curr_visitor.pref_location
        #     if 'sortBy' in request.POST:
        #         if request.POST['sortBy'] == '1':
        #             sortBy = 'avg_rating'
        #         # elif request.POST['sortBy'] == '2':
        #         #     cursor.execute('SELECT id, location from property');
        #         #     prop_list1 = dictfetchall(cursor)
        #         #     prop_list = []
        #         #     url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
        #         #     for i in prop_list1:
        #         #         prop_id = int(i['id'])
        #         #         url += i['location']
        #         #         url += "&destinations="
        #         #         url += preferred_location
        #         #         url += "&key=AIzaSyC6h2gHIWNCKwSNJzBNrYoimC068Ma34KA"
        #         #         req = urllib.request.Request(url)
        #         #         response = urllib.request.urlopen(req)
        #         #         json_data = response.read().decode('ascii')
        #                 # res = json.loads(json_data)
        #         #         for index, i in enumerate(res['rows']):
        #         #             for j in i['elements']:
        #         #                 if j['distance']['value'] > 1000:
        #         #                     cursor.execute('SELECT * FROM property WHERE id = %d', [prop_id]);
        #         #                     answer = dictfetchall(cursor)
                                    
        #         elif request.POST['sortBy'] == '3':
        #             sortBy = 'price'


            if 'query' in request.POST:
                if request.POST['query'] == '1':
                    x = int(request.POST['val'])
                    if 'sortBy' in request.POST:
                        if request.POST['sortBy'] == '1':
                            cursor.execute("""
                                SELECT T.id, T.description, T.price, T.location, T.num_views
                                FROM(SELECT * 
                                     FROM rental_system_property 
                                     WHERE id NOT IN 
                                        (SELECT prop_id_id 
                                         FROM rental_system_rented)) AS T NATURAL JOIN rental_system_review AS R
                                WHERE id IN 
                                    (SELECT prop_id_id 
                                     FROM rental_system_review 
                                     GROUP BY prop_id_id 
                                     HAVING AVG(rating) >= %s)
                                GROUP BY T.id
                                ORDER BY AVG(R.rating) DESC""", [x]);
                        else:
                            cursor.execute("""
                                SELECT T.id, T.description, T.price, T.location, T.num_views
                                FROM(SELECT * 
                                     FROM rental_system_property 
                                     WHERE id NOT IN 
                                        (SELECT prop_id_id 
                                         FROM rental_system_rented)) AS T
                                WHERE id IN 
                                    (SELECT prop_id_id 
                                     FROM rental_system_review 
                                     GROUP BY prop_id_id 
                                     HAVING AVG(rating) >= %s)
                                ORDER BY T.price""", [x])
                    prop_list = dictfetchall(cursor)
                elif request.POST['query'] == '2':
                    print("query 1 being executed")
                    x = int(request.POST['val'])
                    if 'sortBy' in request.POST:
                        if(request.POST['sortBy'] == '1'):
                            cursor.execute("""
                                SELECT T.id, T.description, T.price, T.location, T.num_views
                                FROM(SELECT * 
                                     FROM rental_system_property 
                                     WHERE id NOT IN 
                                        (SELECT prop_id_id 
                                         FROM rental_system_rented)) AS T NATURAL JOIN rental_system_review as R
                                WHERE id IN (SELECT prop_id_id 
                                            FROM rental_system_review 
                                            WHERE rating = 5 
                                            GROUP BY prop_id_id 
                                            HAVING COUNT(rating)>=%s)
                                GROUP BY R.prop_id_id
                                ORDER BY AVG(R.rating) DESC""", [x]);
                        else:
                            cursor.execute("""
                            SELECT T.id, T.description, T.price, T.location, T.num_views
                            FROM(SELECT *
                                 FROM rental_system_property 
                                 WHERE id NOT IN 
                                    (SELECT prop_id_id 
                                     FROM rental_system_rented)) AS T 
                            WHERE id IN (SELECT prop_id_id 
                                        FROM rental_system_review 
                                        WHERE rating = 5 
                                        GROUP BY prop_id_id 
                                        HAVING COUNT(rating)>=%s)
                            ORDER BY T.price""", [x]);
                    prop_list = dictfetchall(cursor)
                elif request.POST['query'] == '3':
                    x = int(request.POST['val'])
                    cursor.execute('SELECT id, location FROM property')#Now it gets linked to the Google API and then gets sorted on the basis of distance
                    prop_list = dictfetchall(cursor)
                elif request.POST['query'] == '4':
                    x = int(request.POST['val'])
                    if 'sortBy' in request.POST:
                        if request.POST['sortBy'] == 1:
                            cursor.execute("""
                                SELECT T.id, T.description, T.price, T.location, T.num_views
                                FROM(SELECT * 
                                     FROM rental_system_property 
                                     WHERE id NOT IN 
                                        (SELECT prop_id_id 
                                         FROM rental_system_rented)) AS T NATURAL JOIN rental_system_review AS R 
                                WHERE price <= %s
                                GROUP BY R.prop_id_id 
                                ORDER BY AVG(R.rating) DESC""", [x])
                        else:
                            cursor.execute("""
                                SELECT T.id, T.description, T.price, T.location, T.num_views
                                FROM(SELECT * 
                                     FROM rental_system_property 
                                     WHERE id NOT IN 
                                        (SELECT prop_id_id 
                                         FROM rental_system_rented)) AS T 
                                WHERE price <= %s
                                ORDER BY T.price""", [x])
                    prop_list = dictfetchall(cursor)

                paginator = Paginator(prop_list, 2)
                page = request.GET.get('page')
                try:
                    property_disp = paginator.page(page)
                except PageNotAnInteger:
                    property_disp = paginator.page(1)
                except EmptyPage:
                    property_disp = paginator.page(paginator.num_pages)
                
    context = {
        'curr_visitor':curr_visitor,
        'properties': property_disp,
        'myprop' : rent_list,
        'error': error
    }
    return render(request, "visitor_dashboard.html", context)

##########################################################
@login_required
def owner_dashboard(request):
    context = {}
    current_user = request.user
    #basically these are SQL QUERIES !!
    current_owner = Owner.objects.get(user = current_user)
    tenants = Rented.objects.filter(owner_id = current_owner)

    # cursor.execute("""SELECT *
    #     FROM rental_system_rented
    #     WHERE owner_id_id = %s""", [current_owner.id]);

    print("I have these tenants - ", tenants)
    properties = Property.objects.filter(owner = current_owner)
    
    # cursor.execute("""SELECT *
    #     FROM rental_system_property
    #     WHERE owner_id = %s""", [current_owner.id]);

    # print(properties)
    if(request.method == "POST"):
        if 'sort' in request.POST:
            if request.POST['sort'] == '1':
                tenants = tenants.order_by('visitor_id')
            elif request.POST['sort'] == '2':
                tenants = tenants.order_by('rent_to_be_paid')
    paginator = Paginator(properties, 2)
    page = request.GET.get('page')
    try:
        property_disp = paginator.page(page)
    except PageNotAnInteger:
        property_disp = paginator.page(1)
    except EmptyPage:
        property_disp = paginator.page(paginator.num_pages)
        
    print(current_owner.owner_name)
    context = {'tenants':tenants,'properties': property_disp}
    return render(request, "owner_dashboard.html",context)

##########################################################

def register(request):
    error = None
    if (request.method =="POST"):
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        existing = User.objects.filter(username__iexact=username)
        # cursor.execute("""SELECT *
        #     FROM rental_system_user
        #     WHERE username_id = %s""", [username.id]);
        
        if existing.exists():
            error = "This username already exists. Kindly provide another username."
        new_user = User.objects.create_user(username = username, password = password, is_owner = True)
        new_user.save()
        new_owner = Owner.objects.create(user = new_user, owner_name = name, num_properties = 0)
        print(new_user)
        new_owner.save()
        return redirect('login')
    return render(request, "register.html",{'error':error})


##########################################################

def register_visitor(request):
    error = None
    if (request.method =="POST"):
        username = request.POST['username']
        password = request.POST['password']
        profile = request.POST['profile']
        pref_location = request.POST['pref_location']
        existing = User.objects.filter(username__iexact=username)
        # cursor.execute("""SELECT *
    #     FROM rental_system_user
    #     WHERE username_id = %s""", [user.id]);

        if existing.exists():
            error = "This username already exists. Kindly provide another username."
            return 
        new_user = User.objects.create_user(username = username, password = password, is_owner = False)
        new_user.save()
        new_visitor = Visitor.objects.create(user = new_user, profile = profile, pref_location = pref_location)
        print(new_user)
        new_visitor.save()
        return redirect('login')
    return render(request, "register_visitor.html",{'error':error})


def view_prop(request, id):
    error = None
    current_user = request.user
    if(current_user.is_owner):
        current_owner = Owner.objects.get(user = current_user)
    else:
        curr_visitor = Visitor.objects.get(user = current_user)
    prop = Property.objects.get(id = id)
    if(not current_user.is_owner):
        prop.num_views += 1
        prop.save()
    review = Review.objects.filter(prop_id = prop)

    # cursor.execute("""SELECT *
    #     FROM rental_system_review
    #     WHERE prop_id_id = %s""", [prop.id]);

    context = {'prop':prop, 
        'review':review, 
        'disp_comment': not current_user.is_owner
        }

    if(not current_user.is_owner):
        if(request.method == "POST"):
            if('rent' in request.POST):
                rented = Rented.objects.create(prop_id = prop,visitor_id=curr_visitor,owner_id=prop.owner,rent_to_be_paid=prop.price)
                rented.save()
                return redirect('dashboard')
            if('form' in request.POST):
                comment = request.POST['comment']
                rating = int(request.POST['rating'])
                rev = Review.objects.create(visitor_id = curr_visitor,prop_id = prop,comment = comment,rating = rating)
                rev.save()
                # return render(request, "view_property.html", context)
    return render(request, "view_property.html", context)

@login_required
def add_property(request):
    error = None
    current_user = request.user
    if(current_user.is_owner):
        current_owner = Owner.objects.get(user = current_user)  
        if request.method == "POST":
            description = request.POST['description']
            price = request.POST['price']
            location = request.POST['location']
            new_prop = Property.objects.create(owner = current_owner, description=description,price=price,location=location)
            new_prop.save()
            return redirect('ownerdashboard')
    else:
        error = "Login as an owner"   
    return render(request, "addProperty.html", {'error':error})

##########################################################

def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request,"home.html",{})