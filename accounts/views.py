import razorpay
from fastzone_main.settings import RZP_KEY_ID, RZP_KEY_SECRET
from django.shortcuts import render,HttpResponse,redirect ,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import CustomUser,Item,CartItem,UserProfile
from orders.utils import generate_order_number
from .forms import MyUserCreationForm
from orders.forms import OrderForm

from .context_processors import get_cart_counter,get_cart_amounts
# Create your views here.

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
def HomeView(request):
    items = Item.objects.all()
    cart_items = CartItem.objects.filter(user= request.user)
    print(cart_items)
    context = {'items':items,"cart_items":cart_items}
    return render(request,'accounts/home.html', context)
    

def RegisterUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,"An Error Occured during registration")

    context = {"form":form}
    return render(request,'accounts/register.html',context)


def LoginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            
        except:
            messages.error(request,"User Not Found")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,'Username or password does not exist')

    return render(request, 'accounts/login.html')


def LogoutUser(request):
    logout(request)
    return redirect('home')


def emailverification(request):
    pass


def ShowItem(request):
    pass
    

def add_to_cart(request,itemId):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest': #check if the request is ajax or not
            #check if the food item exists
            try :
                menuitem = Item.objects.get(id=itemId)
                print(menuitem)
                #Check if user has already added that food to the cart
                try :
                    chkCart = CartItem.objects.get(user=request.user,item_name=menuitem)
                    #Increase cart quantity
                    chkCart.quantity += 1
                    print(chkCart)
                    chkCart.save()
                    return JsonResponse ({'status':'Success','message':'Increased the Cart Quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                
                except:
                    chkCart = CartItem.objects.create(user=request.user,item_name=menuitem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Increased the Cart Quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})

            except:
                return JsonResponse({'status':'Failed','message':'This menuitem doesnot exist'})

        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})

    else:
        return JsonResponse({'status':'Failed','message':'Please login to continue'})


    
    # print(request.POST)
    # item_id = request.POST.get('item_id')
    # print(f"Received item_id: {item_id}")
    # menu_item = get_object_or_404(Item, id=item_id)
    # cart_item, created = CartItem.objects.get_or_create(
    #     user=request.user,
    #     menu_item=menu_item,
    #     defaults={'quantity': 1}
    # )

    # if not created:
    #     cart_item.quantity += 1
    #     cart_item.save()
    # item_name = CartItem.objects.get(id=item_id)
    
    # item_arr = []
    # item_arr.append(item_name) 
    # # cart_count = MenuItem.objects.filter(user=request.user).count()
    
    # response_data = {
    #     'message': 'Item added to cart successfully!',
    #     # 'cart_count': cart_count,
    #     'item_arr' : item_arr,

    # }
    
    # return render(request,'accounts/home.html',response_data)


def cart_view(request):
    cart_items = CartItem.objects.all()
    context = {
        'cart_items' : cart_items,
    }
    return render(request,'accounts/cart.html',context)

def delete_to_cart(request, itemId):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                menuitem = Item.objects.get(id=itemId)
                print(menuitem)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = CartItem.objects.get(user=request.user, item_name=menuitem)
                    
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        print(chkCart)
                        chkCart.save()
                        return JsonResponse ({'status':'Success','message':'Decreased the Cart Quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
def cart_checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
    
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'accounts/checkout.html', context)





def place_order(request):
    cart_items = Item.objects.filter(user=request.user).order_by('created_at')
    print(cart_items)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    # vendors_ids = []
    # for i in cart_items:
    #     if i.fooditem.vendor.id not in vendors_ids:
    #         vendors_ids.append(i.fooditem.vendor.id)
    
    # # {"vendor_id":{"subtotal":{"tax_type": {"tax_percentage": "tax_amount"}}}}
    # get_tax = Tax.objects.filter(is_active=True)
    # subtotal = 0
    # total_data = {}
    # k = {}
    # for i in cart_items:
    #     fooditem = CartItem.objects.get(pk=i.item_name.id)
    #     # v_id = fooditem.vendor.id
    #     if v_id in k:
    #         subtotal = k[v_id]
    #         subtotal += (fooditem.price * i.quantity)
    #         k[v_id] = subtotal
    #     else:
    #         subtotal = (fooditem.price * i.quantity)
    #         k[v_id] = subtotal
    
    #     # Calculate the tax_data
    #     tax_dict = {}
    #     for i in get_tax:
    #         tax_type = i.tax_type
    #         tax_percentage = i.tax_percentage
    #         tax_amount = round((tax_percentage * subtotal)/100, 2)
    #         tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})
    #     # Construct total data
    #     total_data.update({fooditem.vendor.id: {str(subtotal): str(tax_dict)}})
    

        

    subtotal = get_cart_amounts(request)['subtotal']
    # total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    # tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            # order.tax_data = json.dumps(tax_data)
            # order.total_data = json.dumps(total_data)
            # order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            # order.vendors.add(*vendors_ids)
            order.save()

            print(order)
            # RazorPay Payment
            DATA = {
                "amount": float(order.total) * 100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            rzp_order = client.order.create(data=DATA)
            print(rzp_order)
            rzp_order_id = rzp_order['id']

            context = {
                'order': order,
                'cart_items': cart_items,
                'rzp_order_id': rzp_order_id,
                'RZP_KEY_ID': RZP_KEY_ID,
                'rzp_amount': float(order.total) * 100,
            }
            return render(request, 'accounts/place_order.html', context)

        else:
            print(form.errors)
    return render(request, 'accounts/place_order.html')
