from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.mail import send_mail
from django.http import JsonResponse,HttpResponseForbidden
from .models import User, Post, Like, Category
from .forms import RegistrationForm, ResetPasswordForm, PostForm, UserUpdateForm
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


def home(request):    
    blog_posts = Post.objects.all()
    return render(request, 'home.html', {'blog_posts': blog_posts})


def dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('login')

    all_posts = Post.objects.select_related('writer', 'category').all()
    all_likes = Like.objects.select_related('post', 'user').all()

    user_posts = all_posts.filter(writer=user)
    user_likes = all_likes.filter(post__writer=user)

    total_posts = user_posts.count()
    total_likes_received = user_likes.count()

    recent_posts = all_posts.order_by('-created_at')[:5]
    recent_likes = all_likes.order_by('-created_at')[:5]

    total_categories = Category.objects.count()

    context = {
        'user': user,
        'total_posts': total_posts,
        'total_likes_received': total_likes_received,
        'recent_posts': recent_posts, 
        'recent_likes': recent_likes,
        'all_posts': all_posts,
        'all_likes': all_likes,
        'total_categories': total_categories
    }
    return render(request, 'dashboard.html', context)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # print(f"Received email: {email}")
        # print(f"Received password: {password}")

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'login.html')
        try:
            user = User.objects.get(email=email)
            print(f"Stored password: {user.password}")

            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                # request.session['is_admin'] = user.is_admin  

                messages.success(request, 'Logged in successfully.')
                # print("Session data: ", request.session.get('user_id'))     
                # print("Session data: ", request.session.get('is_admin'))     
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong.')
    return render(request, 'login.html')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            reset_token = get_random_string(length=32)
            user.reset_token = reset_token
            user.save()

            reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))
            send_mail('Password Reset', f'Click the link to reset your password: {reset_link}', 'admin@example.com', [email])
            messages.success(request, f'Password reset link sent to your email. Check terminal for the link.')
            print(f'Reset link: {reset_link}')  
            return redirect('password_reset_success')
        else:
            messages.error(request, 'Email does not exist.')
    return render(request, 'forget_password.html')


def password_reset_success(request):
    return render(request, 'password_reset_success.html')
    

def reset_password(request, token):
    user = get_object_or_404(User, reset_token=token)  

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, reset_token=token)
            user.set_password(form.cleaned_data['password'])
            user.reset_token = None  
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


def custom_logout_view(request):
    logout(request)     
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def user_details(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        user = User.objects.get(user_id=user_id)
        return render(request, 'user_details.html', {'user': user})
    else:
        return redirect('login') 


def user_update(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_details')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'user_update.html', {'form': form})


def user_delete(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('register') 
    return render(request, 'user_delete.html')


def create_post(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'You must be logged in to create a post.')
        return redirect('login')

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = user 
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_details', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if not post.public and post.writer != request.user:
        return render(request, '403.html')  
    likes = post.likes.count()
    return render(request, 'post_details.html', {'post': post, 'likes': likes})


def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'You must be logged in to update a post.')
        return redirect('login')
    
    if post.writer.user_id != user_id:
        return HttpResponseForbidden("You do not have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_details', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {'form': form})


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, 'You must be logged in to delete posts.')
        return redirect('login')  

    user = get_object_or_404(User, user_id=user_id)

    if post.writer != user:
        return HttpResponseForbidden('You do not have permission to delete this post.')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'delete_post.html', {'post': post})


def like_post(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)

        user_id = request.session.get('user_id')
        user = get_object_or_404(User, user_id=user_id)  

        like, created = post.likes.get_or_create(user=user, defaults={'name': user.name})
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        likes_count = post.likes.count()

        return JsonResponse({'liked': liked, 'likes_count': likes_count})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
