from django.shortcuts import render ,redirect
from django.http import JsonResponse,HttpResponse
from django.forms import inlineformset_factory
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import OrderForm,CreateUserForm
from django.contrib.auth.decorators import login_required

import requests





def registerPage(request):
    if request.user.is_authenticated:
         return redirect ('store')
    else:
     form=CreateUserForm()
    
     if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Acount was created for"  + user)
            return redirect('login')
           
    context={'form':form}
    return render(request,'store/register.html',context)

def loginPage(request):
     if request.user.is_authenticated:
         return redirect ('store')
     else:
      if request.method=='POST':
       username= request.POST.get('username')
       password= request.POST.get('password')
        
       user=authenticate(request,username= username,password=password)
       if user is not None:
           login(request,user)
           return redirect('store')
           
       else:
           messages.info(request,'username OR password is incorrect')
    
      context={}
     return render(request,'store/login.html',context)
 
def logoutUser(request):
    logout(request)
    return redirect('login')


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

@login_required(login_url='login')
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def initiatekhalti(request):
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        user=request.user

        payload = json.dumps({
            "return_url": "http://127.0.0.1:8000/verify",
            "website_url": "http://127.0.0.1:8000",
            "amount": "1000",
            "purchase_order_id": "sfdfs",
            "purchase_order_name": "test",
            "customer_info": {
                "name": "dfs",
                "email": "es@gmail.com",
                "phone": "98000000001"
            }
        })

        headers = {
            'Authorization': 'Key 4f64f660687f4d1894ee1c1121cfb741',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        new_res=json.loads(response.text)
        print(new_res)
        return redirect(new_res['payment_url'])
    return JsonResponse({'message': 'Payment submitted..', 'response': response.json()}, safe=False)
    
