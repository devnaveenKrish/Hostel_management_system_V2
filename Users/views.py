from django.shortcuts import render, redirect
from cadmin.models import Streets
from cadmin.models import Contact_Form
from cadmin.models import UserType
from cadmin.models import House
from .models import User_Req
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        ph_no = request.POST['ph_no']
        msg = request.POST['msg']
        contact = Contact_Form.objects.create(name=name, email=email, ph_no=ph_no, message=msg)
        contact.save()
        return redirect('index')
    streets = Streets.objects.filter(Street_status=1)
    return render(request , 'Users/main/index.html', {'streets': streets})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            if User_Req.objects.filter(student=user).exists():
                active_users = User_Req.objects.get(student=user)
                if active_users.req_type is 2:
                    print("Yes") 
                else:
                    return redirect('index')
            else:
                pass
            login(request, user)
            return redirect('index')
        else:
            msg = "Wrong Credentaials! Please try again!"
            return render(request, 'Users/login/sign-in.html', {'msg': msg})
    return render(request, 'Users/login/sign-in.html')


def user_registration(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                msg = "Username already exists. Please try another one!"
                return render(request, 'main/signup.html', {'msg':msg})
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)
                user.set_password(password)
                user.save()
                usertype = UserType.objects.create(user=user, usertype='User')
                usertype.save()
                return redirect('user_login')
        else:
            msg = "Passwords do not match. Please try again!"
            return render(request, 'main/signup.html', {'msg':msg})
    return render(request, 'main/signup.html')


def user_logout(request):
    logout(request)
    return redirect('index')


def houses(request, street_id, user_id):
    street = Streets.objects.get(id=street_id)
    houses = House.objects.filter(street=street_id, hs_status=True)
    user_req = User_Req.objects.filter(student=user_id)
    return render(request, 'Users/main/houses.html', {'houses': houses, 'street': street, 'user_req': user_req})

def user_request(request):
    sharing_type = request.POST['sharing_type']
    u_id = request.POST['user_id']
    house_id = request.POST['h_id']
    street_id = request.POST['street_id']
    user_inst = User.objects.get(id=u_id)
    house_inst = House.objects.get(id=house_id)
    print("--------------------*****************###############", street_id)
    print("--------------------*****************###############", u_id)
    print("--------------------*****************###############", house_id)
    req = User_Req.objects.create(student=user_inst, h_id=house_inst, req_type=0, sharing_type=sharing_type)
    req.save()
    return redirect('houses', street_id=street_id, user_id=u_id)

def delete_request(request, req_id):
    req = User_Req.objects.get(id=req_id)
    req.delete()
    return redirect('index')

def reg_hwo(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if cpassword == password:
            if User.objects.filter(username=username).exists():
                msg = "Username already exists! Please try another one!"
                return redirect(reg_hwo)
            user = User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email)
            user.set_password(password)
            user.save()
            user_type = UserType.objects.create(user=user, usertype="House Owner")
            user_type.save()
            return redirect('index')
        else:
            msg = "Password and Comfirm Password didn't match! Please try again!"
            return render(request, 'Users/login/hw_signup.html', {'msg': msg})
    return render(request, 'Users/login/hw_signup.html')







