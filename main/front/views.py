from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main import models
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#---------Paginator_section------------
def paginator_page(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        page = paginator.page(pages)
    except PageNotAnInteger:
        page = paginator.page(1)
    
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page



def index(request):
    if not request.user.is_authenticated:
        return redirect('auth:login') 

    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    wishlist = models.WishList.objects.filter(user=request.user)
    reviews = models.Review.objects.all()
    result = []
    for product in products:
        data = models.WishList.objects.filter(product=product, user=request.user)
        if data:
            product.liked = True
        else:
            product.liked = False
        result.append(product)


    mark = 0
    for i in reviews:
      mark += i.mark
     
    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'categories':paginator_page(categories, 3, request),
        'products':paginator_page(result, 4, request),
        'wishlist':wishlist,
        'rating':range(1,6),
        'mark':mark,
        }

    return render(request, 'front/index.html', context)

#---------Cart_section------------
@login_required(login_url='auth:login')
def add_cart(request, code):
    product = models.Product.objects.get(code=code)
    cart, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    
    try:
        cart_product = models.CartProduct.objects.get(cart=cart, product=product)
        cart_product.count += 1
        cart_product.save()
    except models.CartProduct.DoesNotExist:
        cart_product = models.CartProduct.objects.create(cart=cart, product=product, count=1)

    return redirect('front:index')


@login_required(login_url='auth:login')
def remove_cart(request, code):
    if request.method == 'GET':
        cart = get_object_or_404(models.Cart, user=request.user, status=4)
        product = get_object_or_404(models.Product, code=code)

        cart_products = models.CartProduct.objects.filter(cart=cart, product=product)

        if cart_products.exists():
            cart_products.delete() 

    return redirect('front:active_cart')


@login_required(login_url='auth:login')
def update_quantity(request, code):
    if request.method == 'POST':
        product = models.Product.objects.get(code=code)
        action = request.POST.get('action')
        cart, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
        
        cart_product = models.CartProduct.objects.filter(cart=cart, product=product).first()

        if action == 'increase':
            cart_product.count += 1
        elif action == 'decrease':
            if cart_product.count > 1:
                cart_product.count -= 1
            else:
                cart_product.delete()
                return redirect('front:active_cart')

            cart_product.save()

        return redirect('front:active_cart')



@login_required(login_url='auth:login')
def carts(request):
    queryset = models.Cart.objects.filter(user=request.user, status__in=[2,3,4])
    context = {'queryset':queryset}
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:login')
def active_cart(request):
    queryset , _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    return redirect('front:cart_detail', queryset.code)


@login_required(login_url='auth:login')
def cart_detail(request, code):
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'queryset':queryset
        }
    return render(request, 'front/carts/detail.html', context)


#---------Product_section------------
@login_required(login_url='auth:login')
def product_detail(request,code):
    product = models.Product.objects.get(code=code)
    products = models.Product.objects.all()
    reviews = models.Review.objects.filter(product=product)
    images = models.ProductImg.objects.filter(product=product)
    mark = 0

    for i in reviews:
        mark += i.mark

    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'product':product,
        'products':products,
        'mark':mark,
        'rating':range(1,6),
        'images':images,
        'reviews':reviews,
    }
    return render(request, 'front/product/detail.html',context)


@login_required(login_url='auth:login')
def product_list(request,code=None):
    if code:
        queryset = models.Product.objects.filter(category__code=code)
    else:
        queryset = models.Product.objects.all()
    caregories = models.Category.objects.all()
    context = {
        'queryset':queryset,
        'caregories':caregories,
        }
    return render(request, 'front/category/product_list.html',context)

@login_required(login_url='auth:login')
def product_order(request):
    cart = models.Cart.objects.get(user=request.user, status=1)
    cart_product = models.CartProduct.objects.filter(cart=cart)

    for product in cart_product:
        product.product.quantity -= product.count
        product.product.save()

    cart.status = 2
    cart.save()
    return redirect('front:carts')


#---------Wishlist_section------------
@login_required(login_url='auth:login')
def wishlist(request):
    queryset = models.WishList.objects.filter(user=request.user)
    context = {
        'queryset':queryset
    }
    return render(request, 'front/wishlist/list.html', context)



@login_required(login_url='auth:login')
def add_wishlist(request, code):
    product = get_object_or_404(models.Product, code=code)
    wishlist = models.WishList.objects.filter(product=product, user=request.user)
    if models.WishList.objects.filter(product=product, user=request.user).exists():
        wishlist.delete()
    else:
        wishlist = models.WishList.objects.create(product=product, user=request.user)
    return redirect('front:index')


@login_required(login_url='auth:login')
def remove_wishlist(request, code):
    wishlist = get_object_or_404(models.WishList, product__code=code, user=request.user)
    wishlist.delete()
    return redirect('front:index')


#---------Review_section------------
@login_required(login_url='auth:login')
def add_review(request, code):
    product = models.Product.objects.get(code=code)
    if request.method == 'POST':
        review = models.Review.objects.create(
            product=product,
            user=request.user,
            mark=request.POST.get('review')  
        )
        review.save()
        return redirect('front:cart_detail', code)  
    else:
        return render(request, 'front/carts/detail.html', {'product': product})


