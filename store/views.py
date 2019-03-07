from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from .forms import Login_Form, Add_User_Form, Change_Password_Form, Item_Form
from .models import GUser, Items, Temp, Cart, Order, Order_Final, SUser
from django.db import IntegrityError
from django.core.mail import send_mail
from django.core.paginator import Paginator

def store(request):
    if 'userid' in request.session:
        head = 'Store'
        obj = Items.objects.all()
        paginator = Paginator(obj, 4)
        page = request.GET.get('page')
        items = paginator.get_page(page)
        uid = request.session['userid']
        if request.method == "POST":
            item = request.POST.get('item')
            qnt = request.POST.get("qnt")
            qnt = int(qnt)
            price = Items.objects.get(item_name=item)
            price = price.price
            price = (qnt/1000) * price
            t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
            x = Cart.objects.get(uid=uid)
            x.data.add(t)
            msg = 'items added to cart'
            return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})

        if request.method == "GET":
            cat = request.GET.get('data')
            if cat == "fruits":
                print(cat)
                items = Items.objects.filter(catagorey='fruits') 
                if request.method == "POST":
                    item = request.POST.get('item')
                    qnt = request.POST.get("qnt")
                    qnt = int(qnt)
                    price = Items.objects.get(item_name=item)
                    price = price.price
                    price = (qnt/1000) * price
                    t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
                    x = Cart.objects.get(uid=uid)
                    x.data.add(t)
                    msg = 'items added to cart'
                    return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})

            if cat == "vegetables":
                items = Items.objects.filter(catagorey='vegetables')
                if request.method == "POST":
                    item = request.POST.get('item')
                    qnt = request.POST.get("qnt")
                    qnt = int(qnt)
                    price = Items.objects.get(item_name=item)
                    price = price.price
                    price = (qnt/1000) * price
                    t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
                    x = Cart.objects.get(uid=uid)
                    x.data.add(t)
                    msg = 'items added to cart'
                    return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})

            if cat == "meat":
                items = Items.objects.filter(catagorey='meat')
                if request.method == "POST":
                    item = request.POST.get('item')
                    qnt = request.POST.get("qnt")
                    qnt = int(qnt)
                    price = Items.objects.get(item_name=item)
                    price = price.price
                    price = (qnt/1000) * price
                    t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
                    x = Cart.objects.get(uid=uid)
                    x.data.add(t)
                    msg = 'items added to cart'
                    return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})

            if cat == "nuts":
                items = Items.objects.filter(catagorey='nuts')
                if request.method == "POST":
                    item = request.POST.get('item')
                    qnt = request.POST.get("qnt")
                    qnt = int(qnt)
                    price = Items.objects.get(item_name=item)
                    price = price.price
                    price = (qnt/1000) * price
                    t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
                    x = Cart.objects.get(uid=uid)
                    x.data.add(t)
                    msg = 'items added to cart'
                    return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})

            if cat == "others":
                items = Items.objects.filter(catagorey='others')
                if request.method == "POST":
                    item = request.POST.get('item')
                    qnt = request.POST.get("qnt")
                    qnt = int(qnt)
                    price = Items.objects.get(item_name=item)
                    price = price.price
                    price = (qnt/1000) * price
                    t = Temp.objects.create(item_name=item, quantity=qnt, price=price)
                    x = Cart.objects.get(uid=uid)
                    x.data.add(t)
                    msg = 'items added to cart'
                    return render(request, 'store.html',{'msg':msg,'items':items, 'head':head})


        return render(request, 'store_start.html', {'items':items, 'head':head})
    else:
        return HttpResponseRedirect("/")


def cart(request):
    if 'userid' in request.session:  
        head = 'Cart'    
        uid = request.session["userid"]  
        items = Cart.objects.get(uid=uid) 
        items = items.data.all()
        if request.method =="POST":
            sig = request.POST.get('sig')
            if sig == 'checkout':
                return HttpResponseRedirect("/confirm/")
            else:
                sig = int(sig)
                d = Cart.objects.get(uid=uid) 
                d = items.get(cid=sig)
                d.delete()
                msg = "item removed from cart!" 
                return render(request, 'cart.html', {'items':items, 'msg':msg, 'head':head})
        return render(request, 'cart.html', {'items':items, 'head':head})
    else:
        return HttpResponseRedirect("/")

def add_list(input_list):
    sum = 0
    for item in input_list:
        sum = sum + item
    return sum

def confirm(request):
    head = 'Cart'
    uid = request.session["userid"] 
    user = GUser.objects.get(user_id=uid)
    cart = Cart.objects.get(uid=uid)
    carts = cart.data.all()
    tt = carts.values_list('price', flat=True)
    x = add_list(tt)

    if request.method == "POST":
        status = request.POST.get("confirm")
        if status == "confirm":
            item = cart.data.values_list('item_name', flat=True)
            qnt = cart.data.values_list('quantity', flat=True)
            price = cart.data.values_list('price', flat=True)
            for i,q,p in zip(item,qnt,price):
                fin = Order_Final.objects.get(uid=uid)
                x = Order.objects.create(item_name=i,quantity=q,price=p)
                fin.oid.add(x)
                z = Items.objects.get(item_name=i)
                m = z.stock - q
                z.stock=m
                z.save()

            try:
                email = request.session['email']
                name = request.session['name']
                send_mail(
                'Grocery Emart!',
                name + ' ' + '\n Thank You for Ordering!\n your order confirmed\n',
                'gmarts@gcs.com',
                [email],
                fail_silently=False,
                )
            except:
                msg = "Email service unavailable!"
                return render(request, 'payment.html', {'g':user,'msg':msg, 'head':head, 'cart':carts})         
            
            Temp.objects.all().delete()
            msg = "Order Placed Successfully"
            return render(request, 'confirm.html', {'g':user,'msg':msg, 'head':head})

    return render(request, 'payment.html', {'g':user, 'cart':carts,'x':x, 'head':head})


def about(request):
    head = "About us"
    return render(request, 'about.html', {'head':head})

def add_user(request):
    head = "Signup"
    form = Add_User_Form()
    if request.method == "POST":
        form = Add_User_Form(request.POST or None)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            dob = form.cleaned_data['dob']
            sex = form.cleaned_data['sex']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            try:
                x = GUser.objects.create(name=name,dob=dob,sex=sex,phone=phone,email=email,password=password, address=address)
                z = Cart(uid=x)
                y = Order_Final(uid=x)
                y.save()
                z.save()
                msg = "User Register successfully"
                return render(request, 'register.html', {'form':form, 'msg':msg, 'head':head})
            except IntegrityError:
                msg = "User already exist in database"
                return render(request, 'register.html', {'form':form, 'msg':msg, 'head':head})

        return render(request, 'register.html', {'form':form, 'msg':msg, 'head':head})
    return render(request, 'register.html', {'form':form, 'head':head})


class Staff_Auth(TemplateView):
    template_name = 'staff.html'
    
    def post(self, request):
        head = "Login"
        if 'staffid' not in request.session:
            form = Login_Form(request.POST or None)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                data = [email, password]
                try:
                    email1 = SUser.objects.values_list(
                        "email", flat=True).get(email=email)
                except ObjectDoesNotExist:
                    msg = "Invalid email or password"
                    return render(request, self.template_name, {'form':form, 'msg':msg, 'head':head})
                try:
                    password1 = SUser.objects.values_list("password", flat=True).get(
                        password=password)
                except ObjectDoesNotExist:
                    msg = "Invalid email or password"
                    return render(request, self.template_name, {'form':form, 'msg':msg, 'head':head})
                user = [email1, password1]
                if data == user:
                    did = SUser.objects.get(email=email)
                    request.session["name"] = did.name
                    request.session["email"] = did.email
                    request.session["staffid"] = did.user_id
            return HttpResponseRedirect("/update_items/")         
        else:
            return render(request ,'staff.html', {'head':head}) 
            
    def get(self, request):
        head = "Login"
        if 'staffid' in request.session: 
            return HttpResponseRedirect("/update_items/")
        else:
            form = Login_Form()
            return render(request, self.template_name, {"form": form, 'head':head})



def orders(request):
    head = "Your Orders"
    uid = request.session['userid']
    us = Order_Final.objects.get(uid=uid)
    u = us.oid.all() 
    return render(request, 'orders.html', {'us':us,'u':u, 'head':head})



def add_item(request):
    head = "Add item"
    form = Item_Form()
    if request.method == "POST":
        form = Item_Form(request.POST, request.FILES or None)
        if form.is_valid():
            item = form.cleaned_data["item_name"]
            stock = form.cleaned_data["stock"]
            catagorey = form.cleaned_data["catagorey"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            Items.objects.create(item_name=item, stock=stock, catagorey=catagorey,price=price,image=image)
            msg = "Item added Successfully!"
            return render(request ,'item_add.html', {'form':form,'msg':msg, 'head':head})
    return render(request ,'item_add.html', {'form':form, 'head':head})

def update_item(request):
    head = "Update item"
    if 'staffid' in request.session:
        s = SUser.objects.get(user_id=request.session["staffid"])
        item = Items.objects.all()
        if request.method=="POST":
            item = request.POST.get('item')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            x = Items.objects.get(item_name=item)
            x.stock = stock
            x.price = price
            x.save()
            item = Items.objects.all()
            msg = "item updated successfully!"
            return render(request ,'staff_log.html',{'item':item, 's':s, 'msg':msg, 'head':head})
        return render(request ,'staff_log.html',{'item':item, 's':s, 'head':head}) 
    else:
        return HttpResponseRedirect("/staff_auth/")

class User_Auth(TemplateView):
    template_name = 'home.html'
    
    def post(self, request):
        head = "Login"
        if 'userid' not in request.session:
            form = Login_Form(request.POST or None)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                data = [email, password]
                try:
                    email1 = GUser.objects.values_list(
                        "email", flat=True).get(email=email)
                except ObjectDoesNotExist:
                    msg = "Invalid email or password"
                    return render(request, self.template_name, {'form':form, 'msg':msg, 'head':head})
                try:
                    password1 = GUser.objects.values_list("password", flat=True).get(
                        password=password)
                except ObjectDoesNotExist:
                    msg = "Invalid email or password"
                    return render(request, self.template_name, {'form':form, 'msg':msg, 'head':head})

                user = [email1, password1]
                if data == user:
                    did = GUser.objects.get(email=email)
                    request.session["name"] = did.name
                    request.session["email"] = did.email
                    request.session["userid"] = did.user_id
                    return render(request ,'login.html') 
            return render(request, self.template_name, {"form": form, 'head':head})

        else:
            return render(request ,'login.html',{'head':head}) 
            
    def get(self, request):
        head = "Login"
        if 'userid' in request.session:
            head = "Home"
            return render(request ,'login.html',{'head':head}) 
        else:
            form = Login_Form()
            return render(request, self.template_name, {"form": form, 'head':head})

def user_change_pwd(request):   
    head = "Change Password"
    form = Change_Password_Form()
    if request.method == "POST":
        form = Change_Password_Form(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            try:
                stv = GUser.objects.get(email=email)
            except:
                msg = 'Invalid Email'
                return render(request, 'changepwd.html', {'form':form, 'msg':msg, 'head':head})
            pwd = stv.password
            if password == pwd:
                if email == stv.email:
                    stv.password = new_password
                    stv.save()
                    msg = 'Password Changed Successful'
                    return render(request, 'changepwd.html',{'form': form, 'msg':msg, 'head':head})

    return render(request, 'changepwd.html', {'form': form, 'head':head})


def log_out(request):
    try:
        request.session.flush()
    except KeyError:
        pass
    lg = "logged out"
    return HttpResponseRedirect("/", {'lg':lg})