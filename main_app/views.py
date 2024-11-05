from .models import partners
from django.shortcuts import render, redirect
from .models import User, Enterprises
from django.http import HttpResponse
from django.contrib import messages
from mongoengine.connection import get_db
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Company, MenuItem
from pymongo import MongoClient
from pymongo import DESCENDING
import datetime
from mongoengine import connect
import time
import random
import json
from bson.objectid import ObjectId
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def landing(request):
    Partners = partners.objects.all()
    return render(request, "landing.html", {'Partners': Partners})

def about(request):
    return render(request, "about.html")

def Sign_in(request):
    return render(request, "Sign in.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        role = request.POST.get('Role')

        request.session.flush()

        user = User.objects(username=username).first()

        if 'usern' not in request.session:
            request.session['usern'] = []

        usern = request.session['usern']
        usern.append({
            'username': username,
        })

        request.session['usern'] = usern
        
        if user:
            if user.password == password:
                request.session['logged_in'] = True
                if user.role == role == 'user':
                    return redirect('user_dashboard')
                elif user.role == role == 'supplier':
                    return redirect('supplier_dashboard')
                else:
                    messages.error(request, f"Invalid role for user {username}. Please check your role and try again.")
                    return redirect('Sign_in')
            else:
                messages.error(request, f"Incorrect password for user with username {username}. Please try again.")
                return redirect('Sign_in')
        else:
            messages.error(request, f"User with username {username} does not exist. Please register first.")
            return redirect('Sign_in')

    return render(request, 'Sign in.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        role = request.POST.get('Role')
        
        user_exists = User.objects(username=username).first()
        email_exists = User.objects(email=email).first()

        if user_exists:
            messages.error(request, f"User {username} already exists in the database. Either choose a different username or try logging in")
            return redirect('register')
        elif email_exists:
            messages.error(request, f"Email {email} has already been used. Either choose a different email or try logging in")
            return redirect('register')
        else:
            new_user = User(username=username, email=email, password=password, role=role)
            new_user.save()

            db = get_db()
            user_orders_collection = db[username + '_orders']

            initial_orders_data = {
                'orders': [],
                'user': username,
                'email': email
            }
            user_orders_collection.insert_one(initial_orders_data)
            
            return redirect('Sign_in')
    
    return render(request, 'Sign in.html')

def forgot_password(request):
    if request.method == 'POST':
        enterprise_name = request.POST.get('enterprise_name')
        unique_id = request.POST.get('Unique id')

        client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
        db = client['User_Database']
        collection = db['User Authentication']

        db2 = client['Companies_Database']

        if enterprise_name in db2.list_collection_names():
            enterprise_collection = db2[enterprise_name]

            existing_user = enterprise_collection.find_one({'Ids': unique_id})
            user = collection.find_one({'employee_id': unique_id})

            if existing_user:
                timestamp = int(time.time())
                random_number = random.randint(1000, 9999)
                new_password = f"{timestamp}{random_number}"

                if user:
                    collection.update_one(
                        {'employee_id': unique_id},
                        {'$set': {'password': new_password}}
                    )

                    email = user.get('email')
                    subject = f"Password reset request accepted from {enterprise_name}"
                    message = (
                        f"Hello,\n\nYour new password is: {new_password}. "
                        "Please use this password to sign in, then change it for security purposes."
                    )
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )

                    messages.success(request, "Email with new password has been sent to registered email ID.")
                    return redirect('forgot_password')
            else:
                messages.error(request, "You are not registered in the company's database.")
                return redirect('forgot_password')
        else:
            messages.error(request, f"Collection with name {enterprise_name} does not exist. Enter the correct enterprise name.")
            return redirect('forgot_password')

    return render(request, "forgot-password.html")

def For_enterprises(request):
    return render(request, "for-enterprises.html")

def Enterprise_admin(request):
    if request.method == 'POST':
        enterprise_name = request.POST.get('Enterprise_name')
        email = request.POST.get('Email')
        role = request.POST.get('Role')

        client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
        db = client['Companies_Database']
        enterprise_collection = db[enterprise_name]

        existing_user = enterprise_collection.find_one({'email': email})

        if enterprise_name in db.list_collection_names():
            if existing_user:
                messages.error(request, f"Email {email} has already been used.")
                return redirect('Enterprise_admin')
            else:
                timestamp = int(time.time())
                random_number = random.randint(1000, 9999)
                unique_id = f"{'U' if role == 'user' else 'S'}{timestamp}{random_number}"

                admin_data = {
                    'Ids': unique_id,
                    'enterprise_name': enterprise_name,
                    'email': email
                }
                enterprise_collection.insert_one(admin_data)

                subject = "Your Unique Employee ID from " + enterprise_name
                message = f"Hello,\n\nYour unique ID is: {unique_id}. Please use this ID for accessing the system."
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, f"Unique ID has been generated and sent to {email}.")
                return redirect('Enterprise_admin')
        else:
            messages.error(request, f"Enterprise {enterprise_name} is invalid.")
            return redirect('Enterprise_admin')

    return render(request, 'enterprise-admin.html')


def Enterprise_login(request):
    if request.method == 'POST':
        enterprise_name = request.POST.get('enterprise_name')
        password = request.POST.get('Password')

        request.session.flush()

        user = Enterprises.objects(enterprise_name=enterprise_name).first()

        if 'usern' not in request.session:
            request.session['usern'] = []

        usern = request.session['usern']
        usern.append({
            'enterprise_name': enterprise_name,
        })

        request.session['usern'] = usern
        
        if user:
            if user.password == password:
                request.session['logged_in'] = True
                return render(request, 'enterprise-admin.html')
            else:
                messages.error(request, f"Incorrect password for Enterprise with name {enterprise_name}. Please try again.")
                return redirect('For_enterprises')
        else:
            messages.error(request, f"Enterprise with name {enterprise_name} does not exist. Please register first.")
            return redirect('For_enterprises')

    return render(request, 'for-enterprises.html')


def Enterprise_register(request):
    if request.method == 'POST':
        enterprise_name = request.POST.get('enterprise_name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        
        user_exists = Enterprises.objects(enterprise_name=enterprise_name).first()
        email_exists = Enterprises.objects(email=email).first()

        if user_exists:
            messages.error(request, f"Enterprise {enterprise_name} already exists in the database. Try logging in")
            return redirect('Enterprise_register')
        elif email_exists:
            messages.error(request, f"Email {email} has already been used. Either choose a different email or try logging in")
            return redirect('Enterprise_register')
        else:
            new_user = Enterprises(enterprise_name=enterprise_name, email=email, password=password)
            new_user.save()

            db = get_db(alias='new_database')
            print(db)
            enterprise_collection = db[enterprise_name]

            initial_orders_data = {
                'Ids': [],
                'enterprise_name': enterprise_name,
                'email': email
            }
            enterprise_collection.insert_one(initial_orders_data)
            
            return redirect('For_enterprises')
    
    return render(request, 'for-enterprises.html')

def user_dashboard(request):
    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection_name = f"{username['username']}_orders"
    user_orders_collection = db[collection_name]

    orders = user_orders_collection.find().sort("ordered_at", DESCENDING).limit(10)

    latest_order = list(orders)

    for order in latest_order:
        order['order_id'] = str(order.pop('_id'))

    return render(request, 'user-dashboard.html', {'orders': latest_order})

def user_dashboard_menu(request):
    companies = Company.objects.all()
    selected_company = None
    company_menus = []

    if 'selected_company' in request.session:
        selected_company_name = request.session['selected_company']
        selected_company = get_object_or_404(Company, name=selected_company_name)
        company_menus = MenuItem.objects.filter(company=selected_company)

    if request.method == 'POST':
        company_name = request.POST.get('company')
        selected_company = get_object_or_404(Company, name=company_name)
        request.session['selected_company'] = company_name
        company_menus = MenuItem.objects.filter(company=selected_company)

    return render(request, 'u-db-menu.html', {
        'companies': companies,
        'selected_company': selected_company,
        'company_menus': company_menus,
    })

def user_dashboard_order_history(request):
    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection_name = f"{username['username']}_orders"
    user_orders_collection = db[collection_name]

    orders = user_orders_collection.find().sort("ordered_at", DESCENDING).limit(100)

    all_order = list(orders)

    for order in all_order:
        order['order_id'] = str(order.pop('_id'))

    return render(request, 'u-db-order-history.html', {'orders': all_order})

def user_db_profile(request):
    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection = db['User Authentication']

    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    user_data = collection.find_one(username)

    if user_data:
        if request.method == 'POST':
            employee_id = request.POST.get('Employee ID')
            password = request.POST.get('Password')
            address = request.POST.get('Address')
            contact = request.POST.get('Contact')

            collection.update_one(
                username,
                {
                    '$set': {
                        'employee_id': employee_id,
                        'password': password,
                        'address': address,
                        'contact': contact,
                    }
                }
            )
            return redirect('user_db_profile')

        context = {
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'password': user_data.get('password'),
            'role': user_data.get('role'),
            'e_id': user_data.get('employee_id', ''),
            'address': user_data.get('address', ''),
            'contact': user_data.get('contact', ''),
        }

        return render(request, 'u-db-profile.html', context)

    return render(request, 'u-db-profile.html', {'error': 'User not found'})

def supplier_dashboard(request):
    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection_name = f"{username['username']}_orders"
    user_orders_collection = db[collection_name]

    orders = user_orders_collection.find().sort("ordered_at", DESCENDING)

    latest_order = list(orders)

    for order in latest_order:
        order['order_id'] = str(order.pop('_id'))

    return render(request, 'supplier-dashboard.html', {'orders': latest_order})


def supplier_dashboard_menu(request):
    companies = Company.objects.all()
    selected_company = None
    company_menus = []

    if 'selected_company' in request.session:
        selected_company_name = request.session['selected_company']
        selected_company = get_object_or_404(Company, name=selected_company_name)
        company_menus = MenuItem.objects.filter(company=selected_company)

    if request.method == 'POST':
        company_name = request.POST.get('company')
        selected_company = get_object_or_404(Company, name=company_name)
        request.session['selected_company'] = company_name
        company_menus = MenuItem.objects.filter(company=selected_company)

    return render(request, 's-db-menu.html', {
        'companies': companies,
        'selected_company': selected_company,
        'company_menus': company_menus,
    })

def supplier_db_profile(request):
    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection = db['User Authentication']

    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    user_data = collection.find_one(username)

    if user_data:
        if request.method == 'POST':
            employee_id = request.POST.get('Employee ID')
            address = request.POST.get('Address')
            contact = request.POST.get('Contact')

            collection.update_one(
                username,
                {
                    '$set': {
                        'employee_id': employee_id,
                        'address': address,
                        'contact': contact,
                    }
                }
            )
            return redirect('supplier_db_profile')

        context = {
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'password': user_data.get('password'),
            'role': user_data.get('role'),
            'e_id': user_data.get('employee_id', ''),
            'address': user_data.get('address', ''),
            'contact': user_data.get('contact', ''),
        }

        return render(request, 's-db-profile.html', context)

    return render(request, 's-db-profile.html', {'error': 'User not found'})

def supplier_dashboard_order_history(request):
    if 'usern' in request.session:
        usern = request.session['usern']
        username = usern[0]

    client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
    db = client['User_Database']
    collection_name = f"{username['username']}_orders"
    user_orders_collection = db[collection_name]

    orders = user_orders_collection.find().sort("ordered_at", DESCENDING)

    all_order = list(orders)

    for order in all_order:
        order['order_id'] = str(order.pop('_id'))

    return render(request, 's-db-order-history.html', {'orders': all_order})

def add_to_cart(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(MenuItem, id=item_id)
        quantity = int(request.POST.get('quantity'))

        company_name = menu_item.company.name

        if 'cart' not in request.session:
            request.session['cart'] = []

        cart = request.session['cart']

        cart.append({
            'item_id': str(menu_item.id),
            'name': menu_item.name,
            'quantity': quantity,
            'company': company_name
        })

        request.session['cart'] = cart

        messages.success(request, f'{menu_item.name} added to cart.')

    return redirect('user_dashboard_menu')


def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        address = data.get('address')

        if 'cart' in request.session:
            cart = request.session['cart']

            if not cart:
                messages.error(request, "Your cart is empty. Please add items before placing an order.")
                return JsonResponse({"success": False, "message": "Cart is empty.", "redirect_url": "user_dashboard_menu"})

            if 'usern' in request.session:
                usern = request.session['usern']
                username = usern[0]
            
            client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
            db = client['User_Database']
            collection_name = f"{username['username']}_orders"
            user_orders_collection = db[collection_name]
            collection = db['User Authentication']

            company_names = {item['company'] for item in cart}

            if len(company_names) > 1:
                messages.error(request, "You cannot place an order with items from multiple companies. Please order from only one company.")
                return JsonResponse({"success": False, "message": "Multiple companies error.", "redirect_url": "view_cart"})

            company_of_first_item = list(company_names)[0]

            user_data = collection.find_one(username)

            if user_data and 'employee_id' in user_data and user_data['employee_id']:
                employee_id = user_data['employee_id']

                company_client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
                company_db = company_client['Companies_Database']
                company_collection = company_db[company_of_first_item]

                employee_exists = company_collection.find_one({'Ids': employee_id})
                if not employee_exists:
                    messages.error(request, "Your employee ID does not exist in this company's database. Please contact your company admin.")
                    return JsonResponse({"success": False, "message": "Employee ID not found.", "redirect_url": "view_cart"})

                supplier_data = company_collection.find_one({'Ids': {'$regex': '^S'}})
                if not supplier_data:
                    messages.error(request, "No supplier found for this company.")
                    return JsonResponse({"success": False, "message": "No supplier found.", "redirect_url": "view_cart"})

                supplier_id = supplier_data['Ids']

                order_data_user = {
                    'order_items': cart,
                    'ordered_at': datetime.datetime.now(),
                    'company': company_of_first_item,
                    'status': 'pending',
                    'supplier_id': supplier_id,
                    'reason': '',
                    'name': name,
                    'address': address
                }

                order_data_supplier = {
                    'order_items': cart,
                    'ordered_at': datetime.datetime.now(),
                    'company': company_of_first_item,
                    'status': 'pending',
                    'user_id': employee_id,
                    'reason': '',
                    'name': name,
                    'address': address
                }

                user_orders_collection.insert_one(order_data_user)

                supplier = collection.find_one({'employee_id': supplier_id})
                supplier_name = f"{supplier['username']}_orders"
                supplier_collection = db[supplier_name]

                supplier_collection.insert_one(order_data_supplier)

                del request.session['cart']

                messages.success(request, "Your order has been placed successfully and sent to the supplier.")
                return JsonResponse({"success": True, "redirect_url": "user-dashboard-menu/"})

            else:
                messages.error(request, "Your employee ID is not available. Please update your profile.")
                return JsonResponse({"success": False, "message": "Employee ID not available.", "redirect_url": "cart"})

    return JsonResponse({"success": False, "message": "Invalid request.", "redirect_url": "user-dashboard-menu/"})


def view_cart(request):
    cart = request.session.get('cart', [])

    return render(request, 'add-to-cart.html', {'cart': cart})


def update_cart(request, item_id):
    if request.method == 'POST':

        new_quantity = int(request.POST.get('quantity'))
        

        if 'cart' in request.session:
            cart = request.session['cart']


            for item in cart:
                if item['item_id'] == item_id:
                    item['quantity'] = new_quantity
                    break 

            request.session['cart'] = cart

        return redirect('view_cart')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        if 'cart' in request.session:
            cart = request.session['cart']

            item_name = next((item['name'] for item in cart if item['item_id'] == item_id), None)

            cart = [item for item in cart if item['item_id'] != item_id]
            request.session['cart'] = cart

            if item_name:
                messages.success(request, f'{item_name} has been removed from your cart.')

        return redirect('view_cart')
    
def accept_order(request, order_id):
    if request.method == 'POST':

        if 'usern' in request.session:
            usern = request.session['usern']
            username = usern[0]['username']

        client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
        db = client['User_Database']
        collection = db['User Authentication']

        user_orders_collection = db[f"{username}_orders"]

        Ob_id = ObjectId(order_id)
        object_id_int = int(order_id, 16)

        new_object_id_int = object_id_int - 1

        new_object_id_str = hex(new_object_id_int)[2:].zfill(24)

        new_object_id = ObjectId(new_object_id_str)
        
        order = user_orders_collection.find_one({'_id': Ob_id})

        user_id = order['user_id']
        user = collection.find_one({'employee_id' : user_id})

        user_name = user['username']

        user_collection = db[f"{user_name}_orders"]

        if order and order['status'] == 'pending':
            user_orders_collection.update_one(
                {'_id': ObjectId(order_id)},
                {'$set': {'status': 'accepted'}}
            )

            user_collection.update_one(
                {'_id': ObjectId(new_object_id)},
                {'$set': {'status': 'accepted'}}
            )
            return redirect('supplier_dashboard')
        else:
            return redirect('supplier_dashboard')
    else:
        return redirect('supplier_dashboard')


def reject_order(request, order_id):
    if request.method == 'POST':

        if 'usern' in request.session:
            usern = request.session['usern']
            username = usern[0]['username']

        client = MongoClient('mongodb+srv://SoumikMandal:SM%401819@userdata.q5f9l.mongodb.net/?retryWrites=true&w=majority&appName=UserData')
        db = client['User_Database']
        collection = db['User Authentication']
        
        user_orders_collection = db[f"{username}_orders"]

        Ob_id = ObjectId(order_id)
        object_id_int = int(order_id, 16)

        new_object_id_int = object_id_int - 1

        new_object_id_str = hex(new_object_id_int)[2:].zfill(24)

        new_object_id = ObjectId(new_object_id_str)
        
        order = user_orders_collection.find_one({'_id': Ob_id})

        user_id = order['user_id']
        user = collection.find_one({'employee_id' : user_id})

        user_name = user['username']

        user_collection = db[f"{user_name}_orders"]

        reason = request.POST.get('reason', '')
        if not reason:
            messages.error(request, "Please provide a reason for rejection.")
            return redirect('supplier_dashboard')

        order = user_orders_collection.find_one({'_id': Ob_id})

        if order and order['status'] == 'pending':
            user_orders_collection.update_one(
                {'_id': ObjectId(order_id)},
                {'$set': {'status': 'rejected', 'reason': reason}}
            )

            user_collection.update_one(
                {'_id': ObjectId(new_object_id)},
                {'$set': {'status': 'rejected', 'reason': reason}}
            )
            return redirect('supplier_dashboard')
        else:
            return redirect('supplier_dashboard')
    else:
        return redirect('supplier_dashboard')
