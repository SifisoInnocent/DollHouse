import json
from functools import wraps
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Product, Review, Order, StoreSettings

# Custom Admin Auth Decorator
def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized. Admin credentials required.'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Render Home Page
def index_view(request):
    return render(request, 'shop/index.html')

# --- AUTH APIS ---
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'username': user.username})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def api_auth_status(request):
    is_admin = request.user.is_authenticated and request.user.is_staff
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated,
        'isAdmin': is_admin,
        'username': request.user.username if request.user.is_authenticated else None
    })

# --- PRODUCT APIS ---
def serialize_product(product, request):
    image_url = ""
    if product.image:
        image_url = request.build_absolute_uri(product.image.url)
    return {
        'id': str(product.id),
        'name': product.name,
        'price': float(product.price),
        'category': product.category,
        'inches': product.inches,
        'size': product.size,
        'status': product.status,
        'availDate': product.avail_date,
        'desc': product.desc,
        'image': image_url,
        'createdAt': product.created_at.isoformat()
    }

@csrf_exempt
def api_products(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('-created_at')
        serialized = [serialize_product(p, request) for p in products]
        return JsonResponse(serialized, safe=False)
        
    elif request.method == 'POST':
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            category = request.POST.get('category')
            inches = request.POST.get('inches', '')
            size = request.POST.get('size', '')
            status = request.POST.get('status', 'in-stock')
            avail_date = request.POST.get('avail_date', '')
            desc = request.POST.get('desc', '')
            image = request.FILES.get('image')

            if not name or not price or not category:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                inches=inches,
                size=size,
                status=status,
                avail_date=avail_date,
                desc=desc,
                image=image
            )
            return JsonResponse(serialize_product(product, request), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@admin_required
def api_product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'POST' or request.method == 'PUT':
        # PUT requests might be sent as POST with _method=PUT, or standard multipart
        try:
            # For Django forms/multipart, we can read from request.POST
            product.name = request.POST.get('name', product.name)
            product.price = request.POST.get('price', product.price)
            product.category = request.POST.get('category', product.category)
            product.inches = request.POST.get('inches', product.inches)
            product.size = request.POST.get('size', product.size)
            product.status = request.POST.get('status', product.status)
            product.avail_date = request.POST.get('avail_date', product.avail_date)
            product.desc = request.POST.get('desc', product.desc)
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            return JsonResponse(serialize_product(product, request))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# --- REVIEWS APIS ---
@csrf_exempt
def api_reviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all().order_by('-date')
        data = [{
            'id': str(r.id),
            'name': r.name,
            'text': r.text,
            'rating': r.rating,
            'date': r.date.isoformat(),
            'productId': str(r.product.id) if r.product else None
        } for r in reviews]
        return JsonResponse(data, safe=False)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            text = data.get('text')
            rating = data.get('rating')
            product_id = data.get('productId')
            
            if not name or not text or not rating:
                return JsonResponse({'error': 'Missing fields'}, status=400)
                
            product = None
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    pass
                    
            review = Review.objects.create(
                name=name,
                text=text,
                rating=rating,
                product=product
            )
            return JsonResponse({
                'id': str(review.id),
                'name': review.name,
                'text': review.text,
                'rating': review.rating,
                'date': review.date.isoformat(),
                'productId': str(review.product.id) if review.product else None
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# --- ORDER APIS ---
@csrf_exempt
def api_orders(request):
    if request.method == 'GET':
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        orders = Order.objects.all().order_by('-date')
        data = [{
            'id': str(o.id),
            'product': o.product_summary,
            'customer': o.customer,
            'phone': o.phone,
            'email': o.email,
            'notes': o.notes,
            'channel': o.channel,
            'total': float(o.total),
            'date': o.date.isoformat()
        } for o in orders]
        return JsonResponse(data, safe=False)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = data.get('product', '') # Stored in 'product' field from customer modal or cart items
            customer = data.get('customer', 'Cart Order')
            phone = data.get('phone', '')
            email = data.get('email', '')
            notes = data.get('notes', '')
            channel = data.get('channel', 'whatsapp')
            total = data.get('total', 0.0)

            order = Order.objects.create(
                product_summary=product,
                customer=customer,
                phone=phone,
                email=email,
                notes=notes,
                channel=channel,
                total=total
            )
            return JsonResponse({'id': str(order.id), 'success': True}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# --- STORE SETTINGS APIS ---
@csrf_exempt
def api_settings(request):
    settings = StoreSettings.objects.first()
    if not settings:
        settings = StoreSettings.objects.create()
        
    if request.method == 'GET':
        owner_photo_url = ""
        if settings.owner_photo:
            owner_photo_url = request.build_absolute_uri(settings.owner_photo.url)
        return JsonResponse({
            'key': settings.email_config_key,
            'service': settings.email_config_service,
            'template': settings.email_config_template,
            'ownerEmail': settings.email_config_owner_email,
            'ownerPhoto': owner_photo_url
        })
        
    elif request.method == 'POST':
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        try:
            # Multi-part check (for image uploads)
            if request.content_type.startswith('multipart/form-data') or request.POST:
                settings.email_config_key = request.POST.get('key', settings.email_config_key)
                settings.email_config_service = request.POST.get('service', settings.email_config_service)
                settings.email_config_template = request.POST.get('template', settings.email_config_template)
                settings.email_config_owner_email = request.POST.get('ownerEmail', settings.email_config_owner_email)
                if 'ownerPhoto' in request.FILES:
                    settings.owner_photo = request.FILES['ownerPhoto']
                settings.save()
            else:
                data = json.loads(request.body)
                settings.email_config_key = data.get('key', settings.email_config_key)
                settings.email_config_service = data.get('service', settings.email_config_service)
                settings.email_config_template = data.get('template', settings.email_config_template)
                settings.email_config_owner_email = data.get('ownerEmail', settings.email_config_owner_email)
                settings.save()
                
            owner_photo_url = ""
            if settings.owner_photo:
                owner_photo_url = request.build_absolute_uri(settings.owner_photo.url)
                
            return JsonResponse({
                'success': True,
                'key': settings.email_config_key,
                'service': settings.email_config_service,
                'template': settings.email_config_template,
                'ownerEmail': settings.email_config_owner_email,
                'ownerPhoto': owner_photo_url
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
